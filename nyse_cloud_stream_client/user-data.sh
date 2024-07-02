#!/bin/bash -xe
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
sudo su
sudo yum -y update
sudo yum -y groupinstall "Development Tools"
yum -y install openssl-devel bzip2-devel zlib-devel libffi-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel libpcap-devel xz-devel
sudo yum -y install java-11 git jq wget
sudo yum -y install python3 python3-pip virtualenv
sudo yum -y install protobuf protobuf-compiler
sudo pip3 install virtualenv

wget https://archive.apache.org/dist/kafka/3.5.1/kafka_2.12-3.5.1.tgz
tar -xzf kafka_2.12-3.5.1.tgz
cp -r kafka_2.12-3.5.1 /home/ec2-user/kafka
chown -R ec2-user.ec2-user /home/ec2-user/kafka
cd /home/ec2-user/kafka/libs
wget https://github.com/aws/aws-msk-iam-auth/releases/download/v1.1.1/aws-msk-iam-auth-1.1.1-all.jar

cd /home/ec2-user
su ec2-user -c "git clone https://github.com/aws-samples/NYSE-Cloud-Streaming-Sample-APP.git /home/ec2-user/cloud-streaming-app"
su ec2-user -c "cp -r /home/ec2-user/cloud-streaming-app/client/ /home/ec2-user/kafka-clients/"
su ec2-user -c "protoc -I=/home/ec2-user/kafka-clients/ --python_out=/home/ec2-user/kafka-clients/ /home/ec2-user/kafka-clients/BQT_Cloud_Streaming.proto"
su ec2-user -c "python3 -m venv /home/ec2-user/kafka-clients/.venv"
cd /home/ec2-user/kafka-clients/
source /home/ec2-user/kafka-clients/.venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r /home/ec2-user/kafka-clients/requirements.txt
deactivate

cp /usr/lib/jvm/java-11-amazon-corretto.x86_64/lib/security/cacerts /home/ec2-user/kafka/kafka.client.truststore.jks

cat <<EOF > /home/ec2-user/kafka/client_sasl.properties
security.protocol=SASL_PAINTEXT
sasl.mechanism=SCRAM-SHA-256
ssl.truststore.location=/home/ec2-user/kafka/kafka.client.truststore.jks
EOF
