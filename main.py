from fastapi import FastAPI, HTTPException  # type: ignore
import joblib  # type: ignore
from utils import get_latest_file, log_message
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for lazy-loaded models and data
als_model = knn_model = item_map = inv_item_map = matrix = None

@app.on_event("startup")
def load_models():
    global als_model, knn_model, item_map, inv_item_map, matrix
    try:
        als_model_path = get_latest_file('models', 'als', 'pkl')
        knn_model_path = get_latest_file('models', 'knn', 'pkl')
        item_map_path = get_latest_file('map_data', 'item_map', 'pkl')
        inv_item_map_path = get_latest_file('map_data', 'inv_item_map', 'pkl')
        matrix_path = get_latest_file('matrix_data', 'matrix', 'pkl')

        als_model = joblib.load(als_model_path)
        knn_model = joblib.load(knn_model_path)
        item_map = joblib.load(item_map_path)
        inv_item_map = joblib.load(inv_item_map_path)
        matrix = joblib.load(matrix_path)

        log_message(f"Loaded ALS model from: {als_model_path}")
        log_message(f"Loaded KNN model from: {knn_model_path}")
        log_message(f"Loaded item map from: {item_map_path}")
        log_message(f"Loaded inverse item map from: {inv_item_map_path}")
        log_message(f"Loaded matrix from: {matrix_path}")
    except Exception as e:
        log_message(f"Error loading models on startup: {e}")
        raise RuntimeError("Failed to load necessary models or data files.")

def recommend_similar_audios(audio_id: int, top_n: int = 10) -> dict:
    """Return top N similar audio IDs using ALS with KNN fallback."""

    if any(v is None for v in [als_model, knn_model, item_map, inv_item_map, matrix]):
        log_message("Recommendation requested before models were loaded.")
        return {'data': []}

    if audio_id not in item_map:
        log_message(f"Audio ID {audio_id} not found in training data.")
        return {'data': []}

    item_index = item_map[audio_id]

    # Try ALS-based recommendations
    try:
        item_indices, _ = als_model.similar_items(item_index, N=top_n + 1)
        recs = [inv_item_map[int(idx)] for idx in item_indices if int(idx) != item_index and int(idx) in inv_item_map]
        if recs:
            return {'data': [int(x) for x in recs[:top_n]]}
    except Exception as e:
        log_message(f"ALS failed for Audio ID {audio_id}: {e}, falling back to KNN.")

    # Fallback to KNN
    try:
        distances, indices = knn_model.kneighbors(matrix[item_index], n_neighbors=top_n + 1)
        recs = [inv_item_map[int(i)] for i in indices.flatten() if int(i) != item_index and int(i) in inv_item_map]
        return {'data': [int(x) for x in recs[:top_n]]}
    except Exception as e:
        log_message(f"KNN also failed for Audio ID {audio_id}: {e}.")
        return {'data': []}

@app.get("/recommendations/{audio_id}")
async def get_recommendations(audio_id: int, top_n: int = 10):
    """
    Get audio recommendations for a given audio ID.
    
    Parameters:
    - audio_id: The ID of the audio to get recommendations for
    - top_n: Number of recommendations to return (default: 10)
    
    Returns:
    - JSON response with recommended audio IDs
    """
    try:
        logger.info(f"Fetching recommendations for audio ID: {audio_id}")
        recommendations = recommend_similar_audios(audio_id, top_n)
        
        if not recommendations['data']:
            logger.warning(f"No recommendations found for audio ID: {audio_id}")
            raise HTTPException(status_code=404, detail="No recommendations found")
            
        return recommendations
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
