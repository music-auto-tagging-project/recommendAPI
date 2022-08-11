REGION = "ap-northeast-2"
ECR_PATH = "595017219040.dkr.ecr.ap-northeast-2.amazonaws.com"
ECR_IMAGE = "recommend-api-server"
AWS_CREDENTIAL_ID = "jenkins-aws-moon-credentials"

node{
    stage("CHECKOUT"){
        checkout scm
    }

    stage("DOCKER BUILD"){
        docker.withRegistry("https://${ECR_PATH}","ecr:${REGION}:${AWS_CREDENTIAL_ID}"){
            image = docker.build("${ECR_PATH}/${ECR_IMAGE}","--network=host --no-cache")
        }
    }
    
    stage("TEST"){
        docker.image("${ECR_PATH}/${ECR_IMAGE}").inside{
            sh """python3 -m pytest tests"""
        }
    }

    stage("IMAGE PUSH"){
        docker.withRegistry("https://${ECR_PATH}","ecr:${REGION}:${AWS_CREDENTIAL_ID}"){
            image.push("v${env.BUILD_NUMBER}")
        }
    }

    stage("CLEAN IMAGE"){
        sh"""
        docker rmi ${ECR_PATH}/${ECR_IMAGE}:v$BUILD_NUMBER
        """
    }
}
