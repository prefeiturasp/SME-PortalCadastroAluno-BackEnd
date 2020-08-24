pipeline {
    agent {
      node { 
        label 'py-uniformes'
	    }
    }
    
    options {
      buildDiscarder(logRotator(numToKeepStr: '5', artifactNumToKeepStr: '5'))
      disableConcurrentBuilds()
      skipDefaultCheckout()  
    }
           
    stages {
       stage('CheckOut') {
        steps {
          step([$class: 'GitHubSetCommitStatusBuilder'])
          checkout scm		
        }
       }
       stage('Analise codigo') {
	     when {
           branch 'develop'
         }
            steps {
                sh 'sonar-scanner \
                    -Dsonar.projectKey=SME-PortalCadastroAluno-BackEnd \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=http://sonar.sme.prefeitura.sp.gov.br \
                    -Dsonar.login=72681ab039989ea1be8c9125ffd3db7024e7b913'
            }
       }
      
       stage('Docker Build DEV') {
         when {
           branch 'develop'
         }
        steps {
          sh 'echo build docker image desenvolvimento'
          // Start JOB para build das imagens Docker e push SME Registry
          script {
            step([$class: "RundeckNotifier",
              includeRundeckLogs: true,
              jobId: "7ed3d90c-742f-4391-90b0-d0c3a4258b68",
              nodeFilters: "",
              //options: """
              //     PARAM_1=value1
               //    PARAM_2=value2
              //     PARAM_3=
              //     """,
              rundeckInstance: "Rundeck-SME",
              shouldFailTheBuild: true,
              shouldWaitForRundeckJob: true,
              tags: "",
              tailLog: true])
           }
        }
       }    
                
       
      stage('Deploy DEV') {
         when {
           branch 'develop'
         }
        steps { 
       
           //Start JOB de deploy Kubernetes 
          sh 'echo Deploy ambiente desenvolvimento'
          script {
            step([$class: "RundeckNotifier",
              includeRundeckLogs: true,
              jobId: "0f2a9e05-a65f-4a5a-bbcb-8edb83cafc92",
              nodeFilters: "",
              //options: """
              //     PARAM_1=value1
               //    PARAM_2=value2
              //     PARAM_3=
              //     """,
              rundeckInstance: "Rundeck-SME",
              shouldFailTheBuild: true,
              shouldWaitForRundeckJob: true,
              tags: "",
              tailLog: true])
          }
        } 
       }
       
       stage('Docker Build HOM') {
         when {
           branch 'homolog'
         }
        steps {
          
          script {
            step([$class: "RundeckNotifier",
              includeRundeckLogs: true,
                             
              //JOB DE BUILD
              jobId: "787560d7-f32e-4645-86a1-4eec1159ef57",
              nodeFilters: "",
              //options: """
              //     PARAM_1=value1
               //    PARAM_2=value2
              //     PARAM_3=
              //     """,
              rundeckInstance: "Rundeck-SME",
              shouldFailTheBuild: true,
              shouldWaitForRundeckJob: true,
              tags: "",
              tailLog: true])
          }
        }
       }

       stage('Deploy HOM') {
         when {
           branch 'homolog'
         }
        steps {
          timeout(time: 24, unit: "HOURS") {
          // telegramSend("${JOB_NAME}...O Build ${BUILD_DISPLAY_NAME} - Requer uma aprovação para deploy !!!\n Consulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)\n")
            input message: 'Deseja realizar o deploy?', ok: 'SIM', submitter: 'ebufaino, marcos_nastri, calvin_rossinhole, ollyver_ottoboni, kelwy_oliveira'
          }  
          //Start JOB deploy Kubernetes 
         
          script {
            step([$class: "RundeckNotifier",
              includeRundeckLogs: true,
              jobId: "b52db73e-12cc-4bfa-8249-c875221c61f3",
              nodeFilters: "",
              //options: """
              //     PARAM_1=value1
               //    PARAM_2=value2
              //     PARAM_3=
              //     """,
              rundeckInstance: "Rundeck-SME",
              shouldFailTheBuild: true,
              shouldWaitForRundeckJob: true,
              tags: "",
              tailLog: true])
          }
        }
       }

      stage('Docker Build PROD') {
         when {
           branch 'master'
         }
        steps {
          
          script {
            step([$class: "RundeckNotifier",
              includeRundeckLogs: true,
                             
              //JOB DE BUILD
              jobId: "ea1a4806-c910-4fb7-8a34-afd5177cbc79",
              nodeFilters: "",
              //options: """
              //     PARAM_1=value1
               //    PARAM_2=value2
              //     PARAM_3=
              //     """,
              rundeckInstance: "Rundeck-SME",
              shouldFailTheBuild: true,
              shouldWaitForRundeckJob: true,
              tags: "",
              tailLog: true])
          }
        }
      }

      stage('Deploy PROD') {
         when {
           branch 'master'
         }
        steps {
          timeout(time: 24, unit: "HOURS") {
          // telegramSend("${JOB_NAME}...O Build ${BUILD_DISPLAY_NAME} - Requer uma aprovação para deploy !!!\n Consulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)\n")
            input message: 'Deseja realizar o deploy?', ok: 'SIM', submitter: 'ebufaino, marcos_nastri, calvin_rossinhole, ollyver_ottoboni, kelwy_oliveira'
          }    
          //Start JOB deploy kubernetes 
         
          script {
            step([$class: "RundeckNotifier",
              includeRundeckLogs: true,
              jobId: "c92291f1-8082-4490-96a7-317b1a12a24c",
              nodeFilters: "",
              //options: """
              //     PARAM_1=value1
              //    PARAM_2=value2
              //     PARAM_3=
              //     """,
              rundeckInstance: "Rundeck-SME",
              shouldFailTheBuild: true,
              shouldWaitForRundeckJob: true,
              tags: "",
              tailLog: true])
          }
        }
       }
    } 
  	   
  post {
        always {
          echo 'One way or another, I have finished'
        }
        success {
	  	    step([$class: 'GitHubCommitStatusSetter'])
          telegramSend("${JOB_NAME}...O Build ${BUILD_DISPLAY_NAME} - Esta ok !!!\n Consulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)\n\n Uma nova versão da aplicação esta disponivel!!!")
        }
        unstable {
          step([$class: 'GitHubCommitStatusSetter'])
          telegramSend("O Build ${BUILD_DISPLAY_NAME} <${env.BUILD_URL}> - Esta instavel ...\nConsulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)")
        }
        failure {
          step([$class: 'GitHubCommitStatusSetter'])
          telegramSend("${JOB_NAME}...O Build ${BUILD_DISPLAY_NAME}  - Quebrou. \nConsulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)")
        }
        changed {
          echo 'Things were different before...'
        }
        aborted {
          step([$class: 'GitHubCommitStatusSetter'])
          telegramSend("O Build ${BUILD_DISPLAY_NAME} - Foi abortado.\nConsulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)")
        }
    }
}
