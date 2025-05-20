# Guía para el Tech Day: Práctica con LLM y Terraform

## Parte 1: Entorno con LLM

1. Clona el repositorio o descomprime este paquete.
2. Asegúrate de tener `docker` y `docker-compose` instalados.
3. Ejecuta:
   ```bash
   docker-compose build
   docker-compose run llm
   ```
4. Una vez dentro del contenedor, prueba:
   ```bash
   llm models
   llm --model gemini-pro "¿Qué error tiene este Terraform?"
   ```

## Parte 2: Análisis del error en Terraform

Abre `apply-output.txt`. El error relevante es:

```
Error: creating EC2 Instance: ... InvalidAMIID.NotFound: The image id '[ami-12345678]' does not exist
```

Esto indica que el AMI usado no existe en la región configurada. Se puede preguntar al modelo:

```bash
llm --model gemini-pro "Cómo solucionar el error InvalidAMIID.NotFound en Terraform"
```

Y probar respuestas que sugiere.

## Objetivo

Usar LLM para identificar y resolver errores reales en pipelines de Terraform.
