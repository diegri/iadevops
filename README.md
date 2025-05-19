# Requisitos
- Docker y docker-compose. En sistemas Windows, debe utilizarse el motor de Docker basado en Linux.
- Cuenta GitHub. Se utilizarán funciones de Copilot gratuito
- Nociones de git
- Consola Git Bash (Opcional)
- Visual Studio Code (o portable)

# Demos - Parte 1

## Demo 1.1 - Escribimos código con Copilot

1. Fork a repo Privado

    Repo: https://github.com/diegri/java-web-sample

2. Clone Repo en VS Code

3. Ejecutar Build en local (Opcional)

       docker run -it --rm -v .:/usr/src/javawebsample -v $HOME/.m2:/root/.m2 -w /usr/src/javawebsample maven:3.8.6-openjdk-11 mvn clean install

4. Agregar Copilot en VS (Github Copilot Chat)

5. Chat Copilot: Armado de workflow (test, build, cache)

6. Push and run workflow


## Demo 1.2 - Pipeline CI/CD inteligentes

1. Clonar este repo en local


2. Agregar datos de .env de este repositorio
    
       REPO=tuusuario/tuforkrepo   # Repositorio Privado Demo 1
       RUNNER_TOKEN=token_valido   # Token para self-hosted runner

3. Levantar dockers

       docker-compose -f docker-compose.iarunner.yml build
       docker-compose -f docker-compose.iarunner.yml up -d

4. Cargar modelo LLM

       docker exec -it ollama ollama run qwen2.5-coder:1.5b


5. Checkpoint
   - log runner

         docker container logs runner
   - ollama

         docker exec -it ollama ollama run qwen2.5-coder:1.5b "como se ejecuta un archivo python?"


6. Agregar workflow adicional

    Agregar workflow ubicado en `gh_workflow\build.yml` en el repositorio privado de la Demo anterior.

7. Hacer fallar tests y subir cambio

    Modificar aplicativo para que el resultado sea erroneo.



# Demos - Parte 2

## Demo 2.1. Validar consistencia terraform plan output

N/A

## Demo 2.2 - Assitente DevOps

1. Levantar dockers

       docker-compose -f docker-compose.n8n.yml build
       docker-compose -f docker-compose.n8n.yml up -d

2. Check docker ps command

       docker exec -it n8n docker ps

3. Acceder URL y registrarse

   http://localhost:5678


4. Importar workflow

   Utilzar archivo: `n8n_workflow\docker_assistant.json`


5. Obtener API key

    Obtener API Key de google gemini y configurar en workflow.

6. Chatear con asistente


# Demos - Parte 3

## Demo 3.1 - Simulación de fallo y análisis root cause

1. Levantar dockers 

       cd ai-flame-grahp
       docker compose up --build

2. Acceder a grafana

       http://localhost:3000/

3. Configurar API key

    Acceder en Plugins -> LLM

4. Pedir a IA que explique error

    Acceder a Profiles->Flame Grahp->Explain

# Notas o referencias

## ollama
### WITH GPU
    docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
### CPU ONLY
    docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

### Run model
#### 4.7GB 
    docker exec -it ollama ollama run qwen2.5-coder
#### 1.9GB
    docker exec -it ollama ollama run qwen2.5-coder:3b
#### 986MB
    docker exec -it ollama ollama run qwen2.5-coder:1.5b

### Run questions
#### By command
    docker exec -it ollama ollama run qwen2.5-coder:1.5b "como se ejecuta un archivo python?"

    docker exec -it ollama ollama run qwen2.5-coder:1.5b "Identifica lo que se debe corregir teniendo el siguiente error: $(cat runner_logs/depecheck_error.log)"

#### By API

https://github.com/ollama/ollama/blob/main/docs/api.md

Caso 1

    curl http://ollama:11434/api/chat -s -d '{
      "model": "qwen2.5-coder:1.5b",
      "messages": [
        {
          "role": "user",
          "content": "como se ejecuta un archivo python?"
        }
      ],
      "stream": false
    }' | jq

Caso 2

    curl http://localhost:11434/api/chat -s -d '{
      "model": "qwen2.5-coder:1.5b",
      "prompt": "Cual es el error en el log?",
      "messages": [
        {
          "role": "user",
          "content": "java.lang.AssertionError: Response content expected:<La suma de 5 y 3 es: 8> but was:<La suma de 5 y 3 es: 9>"
        }
      ],
      "stream": false
    }' | jq

Caso 3:
    logError=$(cat runner_logs/output.log | tail -n 30  | jq -Rsa . )

    request='{
        "model": "qwen2.5-coder:1.5b",
        "prompt": "Cual es el error en el log?",
        "messages": [
          {
            "role": "user",
            "content": '$logError'
          }
        ],
        "stream": false
    }'
    echo $request | jq -r '.messages[0].content'
    response=$(curl http://localhost:11434/api/chat -s -d "$request")
    echo $response | jq -r '.message.content'



## n8n

### Docker config

## Grant group access to docker service
docker exec --user root -it n8n chown root:docker /var/run/docker.sock
docker exec --user root -it n8n chmod g+w /var/run/docker.sock
docker exec --user root -it n8n ls -lrt /var/run/docker.sock
