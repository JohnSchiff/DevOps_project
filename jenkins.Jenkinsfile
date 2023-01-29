pipeline {
    agent {
        docker {
            image  '352708296901.dkr.ecr.eu-west-2.amazonaws.com/schiff-jenkins-new-agent:latest'
            args  '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
           REGISTRY_URL = "public.ecr.aws/r7m7o9d4"
           IMAGE_TAG = "0.0.$BUILD_NUMBER"
           IMAGE_NAME = "finalproject-johndaniel"
    }
    stages {
        stage('Build') {
            steps {
                sh '''
                echo "building..."
                aws ecr-public get-login-password --region us-east-1  | docker login --username AWS --password-stdin $REGISTRY_URL
                docker build -t $IMAGE_NAME:$IMAGE_TAG . -f Dockerfile
                docker tag $IMAGE_NAME:$IMAGE_TAG $REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG
                docker push $REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG
                echo "done"
                '''
            }
        }
        stage('Run') {
            steps {
                sh 'docker pull $REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG'
                sh 'docker run -p 8501:8501 $REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG'
            }
        }
    }
}