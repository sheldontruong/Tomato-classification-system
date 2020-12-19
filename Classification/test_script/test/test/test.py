from tensorflow.keras.models import load_model
import tensorflow as tf
from utils import *

def main():
    #change dir and load model
    os.chdir("D:/4.DO AN CDT/code_test")
    model = load_model("trained_model/weights.100.66-0.98.h5") 
    #get session of model to use in gradCAM computing
    sess = tf.keras.backend.get_session()
    #run real time process
    test_vid("camera",model,sess)

if __name__ == '__main__':
    main()

