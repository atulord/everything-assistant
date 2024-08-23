import pytest
from unittest.mock import patch, mock_open
import json
import pandas as pd
from utils import load_json, load_csv, save_json

def test_load_json():
    mock_data = '{"key": "value"}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = load_json("dummy_path.json")
        assert result == {"key": "value"}

def test_load_csv():
    mock_csv_data = "column1,column2\nvalue1,value2"
    expected_json = '[{"column1":"value1","column2":"value2"}]'
    
    with patch("pandas.read_csv") as mock_read_csv:
        mock_df = pd.DataFrame([{"column1": "value1", "column2": "value2"}])
        mock_read_csv.return_value = mock_df
        result = load_csv("dummy_path.csv")
        assert json.loads(result) == json.loads(expected_json)

@patch("json.dump")
@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_save_json(mock_makedirs, mock_file, mock_json_dump):
    data = {"key": "value"}
    filename = "path/to/file.json"
    
    save_json(data, filename)
    
    mock_makedirs.assert_called_once_with("path/to", exist_ok=True)
    mock_file.assert_called_once_with(filename, 'w')
    mock_json_dump.assert_called_once_with(data, mock_file(), indent=4)

# Add more tests if needed