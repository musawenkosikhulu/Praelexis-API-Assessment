from fastapi import FastAPI, HTTPException
from typing import List
import pandas as pd

app = FastAPI()

@app.post("/survivorCount")
async def survivor_count(data: dict):
    try:
        # Extracting required data
        passengers = data['data']
        bin_boundaries = data['binBoundaries']
        bin_field = data['binField']

        # Check if binField is numeric
        if not is_numeric_field(passengers, bin_field):
            raise HTTPException(status_code=404, detail=f"{bin_field} is not a numeric field.")

        # Transformation
        counts = count_survivors(passengers, bin_boundaries, bin_field)

        return {'counts': counts}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def is_numeric_field(passengers, bin_field):
    # Check if the specified bin field is numeric
    for passenger in passengers:
        if not isinstance(passenger.get(bin_field), (int, float)):
            return False
    return True

def count_survivors(passengers, bin_boundaries, bin_field):
    # Initialize counts for each bin
    counts = [0] * (len(bin_boundaries) + 1)

    # Count survivors in each bin
    for passenger in passengers:
        age = passenger.get(bin_field, 0)
        bin_index = get_bin_index(age, bin_boundaries)
        
        counts[bin_index] += 1 if passenger.get('Survived') == 1 else 0

    return counts

def get_bin_index(value, bin_boundaries):
    # Get the bin index based on bin boundaries
    for i, boundary in enumerate(bin_boundaries):
        if value < boundary:
            return i
    return len(bin_boundaries)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
