"""
Dataset loading and preprocessing utilities
"""
import json
import pandas as pd
from pathlib import Path
from typing import List, Tuple, Dict, Any
from sklearn.model_selection import train_test_split


class DatasetLoader:
    """
    Utility class for loading and preprocessing datasets
    """
    
    def __init__(self, dataset_path: str):
        """
        Initialize the dataset loader
        
        Args:
            dataset_path: Path to the dataset JSON file
        """
        self.dataset_path = Path(dataset_path)
        self.data = None
        self.df = None
    
    def load_dataset(self) -> pd.DataFrame:
        """
        Load the dataset from JSON file
        
        Returns:
            DataFrame with the loaded data
        """
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Dataset file not found: {self.dataset_path}")
        
        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.df = pd.DataFrame(self.data)
        
        # Handle missing values
        self.df = self.df.fillna('')
        
        print(f"Dataset loaded: {len(self.df)} samples")
        print(f"Classes: {self.df['tag'].unique()}")
        print(f"Class distribution:\n{self.df['tag'].value_counts()}")
        
        return self.df
    
    def get_texts_and_labels(self) -> Tuple[List[str], List[str]]:
        """
        Get texts and labels from the dataset
        
        Returns:
            Tuple of (texts, labels)
        """
        if self.df is None:
            self.load_dataset()
        
        return self.df["content"].tolist(), self.df["tag"].tolist()
    
    def get_training_data(self) -> Tuple[List[str], List[str]]:
        """
        Get training data (80% of dataset) - same as original script
        
        Returns:
            Tuple of (X_train, y_train)
        """
        if self.df is None:
            self.load_dataset()
        
        X = self.df["content"]
        y = self.df["tag"]
        
        X_train, _, y_train, _ = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=42
        )
        
        return X_train.tolist(), y_train.tolist()
    
    def get_train_test_split(self, test_size: float = 0.2, random_state: int = 42) -> Tuple[List[str], List[str], List[str], List[str]]:
        """
        Get train-test split of the dataset
        
        Args:
            test_size: Proportion of data to use for testing
            random_state: Random seed for reproducibility
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        if self.df is None:
            self.load_dataset()
        
        X = self.df["content"]
        y = self.df["tag"]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, stratify=y, random_state=random_state
        )
        
        return X_train.tolist(), X_test.tolist(), y_train.tolist(), y_test.tolist()
    
    def get_dataset_info(self) -> Dict[str, Any]:
        """
        Get information about the dataset
        
        Returns:
            Dictionary with dataset statistics
        """
        if self.df is None:
            self.load_dataset()
        
        return {
            "total_samples": len(self.df),
            "num_classes": self.df["tag"].nunique(),
            "classes": self.df["tag"].unique().tolist(),
            "class_distribution": self.df["tag"].value_counts().to_dict(),
            "avg_text_length": self.df["content"].str.len().mean(),
            "min_text_length": self.df["content"].str.len().min(),
            "max_text_length": self.df["content"].str.len().max()
        }
