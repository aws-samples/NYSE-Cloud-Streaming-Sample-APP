import os, boto3
from aws_cdk import (
    Stack,Tags,Fn,CfnTag,CfnOutput,
    aws_ec2 as ec2,
    aws_route53 as route53
)
from constructs import Construct

from . import config

vpc_azs = []
class NyseCloudStreamClientStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get AZ Name out of AZ IDs
        client = boto3.client('ec2')
        azs = client.describe_availability_zones(ZoneIds=config.vpc_azs_ids)
        x=0
        for az in azs.get('AvailabilityZones'):
            for az_id in config.vpc_azs_ids:
                if az_id == az.get('ZoneId'):
                    vpc_azs.append(az.get('ZoneName'))
            x += 1

        # Create CloudStream consumer VPC
        cloudstream_vpc = ec2.Vpc(self, "cloud_stream_vpc",
            vpc_name="Cloud Stream VPC",
            ip_addresses= ec2.IpAddresses.cidr(config.vpc_cidr),
            nat_gateways=1,
            availability_zones=vpc_azs,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    cidr_mask=24,
                    name="Cloud Stream - Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    map_public_ip_on_launch=False,
                ),
                ec2.SubnetConfiguration(
                    cidr_mask=24,
                    name="Cloud Stream - Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                ),
            ],
        )

        # Create security group for VPC
        vpc_security_group = ec2.SecurityGroup(self, "cloud_stream_sg",
            vpc=cloudstream_vpc,
            description="NYSE Cloud Stream security group",
            security_group_name="Cloud Stream SG",
            allow_all_outbound=True,
        )
        vpc_security_group.add_ingress_rule(ec2.Peer.ipv4(config.vpc_cidr), ec2.Port.tcp(22), "Allow access to SSH port from within the VPC")
        vpc_security_group.add_ingress_rule(ec2.Peer.ipv4(config.vpc_cidr), ec2.Port.tcp(9092), "Allow access to 9092 port from within the VPC")

        # Private Hosted Zone
        private_zone = route53.PrivateHostedZone(self, "cloud_stream_HostedZone", 
            zone_name=config.feed_domain_name, vpc=cloudstream_vpc
        )

        # Add VPC Interface endpoints to vpc and DNS Entries
        x=0
        for endpoint_service_id in config.endpoint_service_ids:
            endpoint = cloudstream_vpc.add_interface_endpoint("Cloud Stream Endpoint"+str(x), service=ec2.InterfaceVpcEndpointService(endpoint_service_id,9092), subnets=ec2.SubnetSelection(availability_zones=[vpc_azs[x]]))
            Tags.of(endpoint).add("Name", "Cloud Stream - Endpoint"+str(x))
            endpoint_dns=Fn.split(":",Fn.select(0, endpoint.vpc_endpoint_dns_entries),assumed_length=2)
            route53.CnameRecord(self, "AliasRecord"+str(x), 
                zone=private_zone, 
                record_name="broker"+str(x+1), 
                domain_name=endpoint_dns[1]
            )
            x +=1

        # Create an EC2 instance connect endpoint
        instance_connect_endpoint = ec2.CfnInstanceConnectEndpoint(self, "InstanceConnectEndpoint",
            subnet_id=cloudstream_vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnets[1].subnet_id,
            preserve_client_ip=False,
            security_group_ids=[vpc_security_group.security_group_id],
            tags=[CfnTag(key="Name",value="CloudStream - InstanceConnectEndpoint")]
        )

        # Create an EC2 instance in this  VPC to run the Kafka feed consumer app
        # EC2 Instance BootStrap configuration  
        user_data_path = os.path.join(os.path.dirname(__file__), "user-data.sh")
        with open(user_data_path, encoding='utf-8') as f:
            user_data = f.read()

        # Create an EC2 instance keypair
        key_pair = ec2.KeyPair.from_key_pair_attributes(self, "KeyPair",
            key_pair_name=config.ec2_key_pair,
            type=ec2.KeyPairType.RSA
        )

        # EC2 Instance definition
        instance = ec2.Instance(self, "cloud_stream_consumer_instance1",
            instance_type = ec2.InstanceType("t3.large"),
            instance_name = "CloudStream - Consumer Instance",
            machine_image = ec2.MachineImage.latest_amazon_linux2023(),
            security_group = vpc_security_group,
            vpc = cloudstream_vpc,
            vpc_subnets=ec2.SubnetSelection(availability_zones=vpc_azs),
            availability_zone=vpc_azs[1],
            user_data=ec2.UserData.custom(user_data),
            key_pair = key_pair,
        )
        
        instance.user_data.add_commands(
            f"echo \"export BROKERS={','.join(config.bootstrap_brokers)}\" >> /home/ec2-user/.bashrc \n",
            "cd /home/ec2-user",
            "cat <<EOF > /home/ec2-user/kafka/users_jaas.conf",
            "KafkaClient {",
            f"    org.apache.kafka.common.security.scram.ScramLoginModule required",
            f'    username="{config.cloudstream_username}"',
            f'    password="{config.cloudstream_password}";',
            "};",
            "EOF",
            f'echo \"export KAFKA_SASL_USERNAME={config.cloudstream_username}\" >> /home/ec2-user/.bashrc \n',
            f'echo \"export KAFKA_SASL_PASSWORD={config.cloudstream_password}\" >> /home/ec2-user/.bashrc \n',
            f'echo \"export KAFKA_GROUP_ID={config.cloudstream_group_id}\" >> /home/ec2-user/.bashrc \n',
            f'echo \"export KAFKA_TOPICS={','.join(config.cloudstream_topics)}\" >> /home/ec2-user/.bashrc \n',
            f'echo \"export KAFKA_OPTS=-Djava.security.auth.login.config=/home/ec2-user/kafka/users_jaas.conf\" >> /home/ec2-user/.bashrc \n',
        )

        ## CDK Output instance id
        CfnOutput(self, "InstanceID", value=instance.instance_id)