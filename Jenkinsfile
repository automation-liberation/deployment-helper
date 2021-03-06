def label = "worker-${UUID.randomUUID().toString()}"
def properties

podTemplate(label: label, containers: [
    containerTemplate(name: 'python', image: 'python:3.7', command: 'cat', ttyEnabled: true),
    containerTemplate(name: 'docker', image: 'docker', command: 'cat', ttyEnabled: true)
    ],
    volumes: [
    hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock')
    ], imagePullSecrets: [ 'docker-registry-credentials' ]
  ) {
    node(label) {
        stage('Build') {
            git 'https://github.com/automation-liberation/deployment-helper.git'
            script {
                properties = readYaml file: "build-properties.yaml"
            }
            container('python') {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Push Docker Image') {
            container('docker') {
                withCredentials([[$class: 'UsernamePasswordMultiBinding',
                    credentialsId: 'irori',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASSWORD']]) {
                    sh """
                        docker login -u ${USER} -p ${PASSWORD} https://${properties.image.registry}
                        docker build -t ${properties.image.registry}/${properties.image.package}:${properties.image.tag} .
                        docker tag ${properties.image.registry}/${properties.image.package}:${properties.image.tag} ${properties.image.registry}/${properties.image.package}:latest
                        docker push ${properties.image.registry}/${properties.image.package}
                    """
                }
                sh "docker rmi ${properties.image.registry}/${properties.image.package}:${properties.image.tag}"
            }
        }
    }
}
