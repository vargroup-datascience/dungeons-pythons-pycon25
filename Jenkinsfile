pipeline{

    agent{ label "k8s-agent-raw"}
    environment{
        DOCKER_OPTS = "-u root --network host -e DOCKER_HOST=tcp://localhost:2375"
        DOCKER_REGISTRY = 'https://index.docker.io/v1/'                                             
        DOCKER_CREDENTIALS = 'docker-hub-credentials'                                               
        GIT_REPO_NAME = env.GIT_URL.replaceFirst(/^.*\/([^\/]+?).git$/, '$1')                       
        GIT_SSH_KEY = 'bitbucket-ssh-key-for-private-repo'                                         
        RUNNER_IMAGE = 'analyticsnetworksrl/an_runners:python-3.12'             
    }
    parameters {
        booleanParam(
            name: 'FORCE_BUILD_AND_RELEASE',
            defaultValue: false,
            description: '🥶 Force build and image release regardless of tests conditions.'
        )
    }

    stages{
        stage('Init'){
            steps {
                script {
                    env.REPO_NAME = env.GIT_REPO_NAME ?: error("GIT_REPO_NAME is not set.")
                    env.IMAGE_TAG = "dev"
                    env.DOCKER_FILE_FOLDER = "."
                    env.FULL_IMAGE_NAME = "analyticsnetworksrl/${env.REPO_NAME}:${env.IMAGE_TAG}"
                    env.AUTHOR_MAIL = computeAuthorName()
                }
            }
        }
        stage('Entriamo nel Dungeon') {
            when {
                branch 'main'
            }
            steps {
                script {
                    try{buildImage()}
                    catch (err) {error "Failed to build Docker image: ${env.FULL_IMAGE_NAME}"}

                    docker.image(env.FULL_IMAGE_NAME).inside(DOCKER_OPTS) {
                        try {
                            sh "sleep 10"
                            sh "curl -s --fail http://localhost:5000 > /dev/null"
                        }
                        catch (err) {error "Streamlit is not inside this cave"}
                    }

                    try {releaseImage()}
                    catch (err) {error "Failed to push Docker image: ${env.FULL_IMAGE_NAME} to Docker Hub."}
                }
            }
        }
    }
    post {
        always {
            cleanWs()
            script {
                emailext(
                    subject: "Build Finished [${currentBuild.currentResult}]: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: "Check logs: ${env.BUILD_URL}",
                    to: env.AUTHOR_MAIL
                )
            }
        }
    }
}

def computeAuthorName() {
    return sh(script: "git log -1 --pretty=format:'%ae'", returnStdout: true).trim()
}

def buildImage(){
    script {
        try {
            sshagent (credentials: [env.GIT_SSH_KEY]) {
                sh " docker build --ssh default -t ${env.FULL_IMAGE_NAME} ${env.DOCKER_FILE_FOLDER}"
            }
            echo "Built Docker image: ${env.FULL_IMAGE_NAME}"
        } catch (err) {
            error "Failed to build Docker image: ${env.FULL_IMAGE_NAME}"
        }
    }
}

def releaseImage(){
    script {
        try {
            docker.withRegistry(env.DOCKER_REGISTRY, env.DOCKER_CREDENTIALS) {
                sh "docker push ${env.FULL_IMAGE_NAME}"
            }
            echo "Successfully pushed Docker image: ${env.FULL_IMAGE_NAME} to Docker Hub."
        } catch (err) {
            error "Failed to push Docker image: ${env.FULL_IMAGE_NAME} to Docker Hub."
        }
    }
}