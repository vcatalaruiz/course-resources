from transformers import AutoTokenizer, AutoModelForCausalLM

# Nombre del modelo que queremos utilizar (Phi-2 en este caso)
model_name = "microsoft/Phi-2"

# Directorio local donde se guarda el modelo para no descargarlo cada vez
cache_dir = "./model_cache"

# Carga del tokenizer desde la carpeta local
# El tokenizer convierte texto → números (tokens)
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)

# Carga del modelo desde la carpeta local
# Este es el modelo neuronal que generará texto
model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=cache_dir)

# Función para generar respuestas usando el modelo
def chat(prompt):
    # Convertimos el texto (prompt) en tensores para PyTorch
    tokens = tokenizer(prompt, return_tensors="pt")
    
    # Generamos texto a partir del modelo
    output = model.generate(
        tokens["input_ids"],   # tokens de entrada
        max_length=150,        # longitud máxima total (prompt + respuesta)
        temperature=0.2,       # determina creatividad (baja = respuestas más precisas)
        do_sample=False,       # False = determinista (sin muestreo aleatorio)
        top_p=0.9              # filtrado por probabilidad acumulada
    )
    
    # Convertimos los tokens de salida a texto nuevamente
    return tokenizer.decode(output[0], skip_special_tokens=True)

# Pedimos al usuario que escriba una pregunta
question = input("Escribe tu pregunta: ")

# Creamos el prompt que se envía al modelo
# Le damos instrucciones y le pasamos la pregunta del usuario
prompt = (
    "Answer the following question with a short factual answer.\n"
    f"Question: {question}\n"
    "Answer:"
)

# Ejecutamos el modelo y mostramos la respuesta final
print(chat(prompt))