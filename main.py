from fastapi import FastAPI, File
from pydantic import BaseModel
import xgboost as xgb
import numpy as np
import pickle
import warnings
import base64
from PIL import Image
import io

# Ignorar warnings desnecessários
warnings.simplefilter(action='ignore', category=DeprecationWarning)

# Inicializando o aplicativo FastAPI
app = FastAPI()

# Definição dos tipos de dados para resposta e requisição
class PredictionResponse(BaseModel):
    prediction: float

class ImageRequest(BaseModel):
    image: str  # A imagem será enviada como uma string em base64

# Carregar o modelo XGBoost
def load_model():
    global xgb_model_carregado
    with open("models/xgboost_model.pkl", "rb") as f:
        xgb_model_carregado = pickle.load(f)

# Inicializar o modelo quando o servidor iniciar
@app.on_event("startup")
async def startup_event():
    load_model()

# Rota de inferência para previsão
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: ImageRequest):
    # Decodificar a imagem recebida em base64
    img_bytes = base64.b64decode(request.image)
    img = Image.open(io.BytesIO(img_bytes))
    
    # Redimensionar a imagem para o tamanho correto (8x8)
    img = img.resize((8, 8))
    
    # Converter a imagem em array numpy
    img_array = np.array(img)
    
    # Converter para escala de cinza
    img_array = np.dot(img_array[...,:3], [0.2989, 0.5870, 0.1140])
    
    # Redimensionar o array para o formato correto para o modelo
    img_array = img_array.reshape(1, -1)
    
    # Fazer a predição
    prediction = xgb_model_carregado.predict(img_array)
    
    # Retornar a predição
    return {"prediction": float(prediction[0])}

# Endpoint para healthcheck
@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
