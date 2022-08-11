pipeline{
    agent any

    environment{
        REGION = "ap-northeast-2"
        ECR_PATH = "595017219040.dkr.ecr.ap-northeast-2.amazonaws.com"
        ECR_IMAGE = "recommend-api-server"
        AWS_CREDENTIAL_ID = "jenkins-aws-moon-credentials"
    }
    
    parameters{
        string(name: 'BUILD_NUM', defaultValue: 'latest', description: 'docker image build number')
    }

    stages{
        stage("INITAL"){
            steps{
                echo "INITIALIZING..."
            }
        }

        stage("DOCKER BUILD"){
            steps{
                script{
                    docker.withRegistry("https://${ECR_PATH}","ecr:${REGION}:${AWS_CREDENTIAL_ID}"){
                       image = docker.build("${ECR_PATH}/${ECR_IMAGE}","--network=host --no-cache .")}
                }
            }
        }

        stage("TEST"){
            steps{
                script{
                    docker.image("${ECR_PATH}/${ECR_IMAGE}").inside{
                        sh """python3 -m pytest tests"""}
                }
            }
        }

        stage("IMAGE PUSH"){
            steps{
                script{
                    docker.withRegistry("https://${ECR_PATH}","ecr:${REGION}:${AWS_CREDENTIAL_ID}"){
                        image.push("v${params.BUILD_NUM}")}
                }
            }
        }
    }
    post{
        always{
            script{
                sh"""
                docker rmi ${ECR_PATH}/${ECR_IMAGE}:v${params.BUILD_NUM}
                docker rmi ${ECR_PATH}/${ECR_IMAGE}:latest
                """
            }
        }
    }
}
