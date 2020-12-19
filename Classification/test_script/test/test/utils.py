import cv2
import numpy as np
import os
import tensorflow as tf
import time
import screeninfo
import h5py

def bottleneck_res_block(block_input,factor):
  ###expansion convolution layer
  x = tf.keras.layers.Conv2D(int(factor)*int(block_input.shape[3]),(1,1))(block_input) 
  x = tf.keras.layers.BatchNormalization()(x)
  x = tf.keras.layers.ReLU(max_value = 6)(x)
  #x = tf.keras.layers.Dropout(rate = 0.3)(x)
  ###depthwise convolution layer
  x = tf.keras.layers.DepthwiseConv2D((3,3),padding = 'same')(x)
  x = tf.keras.layers.BatchNormalization()(x)
  x = tf.keras.layers.ReLU(max_value = 6)(x)
  #x = tf.keras.layers.Dropout(rate = 0.3)(x)
  ###projection convolution layer
  x = tf.keras.layers.Conv2D(int(int(x.shape[3])/int(factor)),(1,1))(x)
  x = tf.keras.layers.BatchNormalization()(x)
  x = tf.keras.layers.ReLU(max_value = 6)(x)
  #x = tf.keras.layers.Dropout(rate = 0.3)(x)
  #Residual connect
  x = tf.keras.layers.Add()([x,block_input])
  
  return x
def model_test():
    x_in = tf.keras.layers.Input((224,224,3))
    x = tf.keras.layers.Conv2D(32,(1,1))(x_in)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.MaxPool2D((2,2))(x)
    x = tf.keras.layers.ReLU(6)(x)
    x = tf.keras.layers.Dropout(rate = 0.6)(x)
    x = bottleneck_res_block(x,2)
    x = tf.keras.layers.AveragePooling2D((2,2))(x)
    x = bottleneck_res_block(x,2)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(5,activation = 'softmax')(x)
    model = tf.keras.models.Model(inputs = x_in, outputs = x)
    model.compile(optimizer ='adam', loss = 'categorical_crossentropy',metrics = ['accuracy'])
    return model
def test_set(model):
    test_dir = "cachua_resize2/test/"
    test_list = os.listdir(test_dir)
    test_img_list = [os.listdir(test_dir+folder) for folder in test_list]
    x_test = []
    y_test = []
    for label in range(len(test_img_list)):
        y_now = np.zeros((6,))
        y_now[label] = 1
        for idx in range(len(test_img_list[label])):
            img = cv2.imread(test_dir+test_list[label]+"/"+test_img_list[label][idx])
            img = cv2.resize(img,(100,100))
            img = img/255
            x_test.append(img)
            y_test.append(y_now)
    x_test = np.asarray(x_test)
    y_test = np.asarray(y_test)
    model.summary()
    print(x_test.shape)
    print(y_test.shape)
    outcome = model.evaluate(x = x_test,y = y_test)
    print("Model's Accuracy on test set is: "+str(outcome[1]))
    return outcome
def test_img_adr(adr,model):
    """
    Argument:
        ___adr: type is String. Address of image
        ___model: type is Keras model
    Output:
        ___predict: a np.array() show probability of n class in model
    """
    img = cv2.imread(adr)
    predict = test_img(np.asarray(img),model)
    cv2.imshow("cachua",cv2.resize(img,(400,400)))
    print("Image address: "+adr)
    print("loai "+str(np.argmax(predict)+1)+":"+str((predict)))
    cv2.waitKey(0)
    return predict

################################REAL TIME######################################
def test_img(img, model):
    """
    Argument:
        ___img: type is np.array(). 
        ___model: type is Keras model
    """
    img = cv2.resize(img,(100,100))
    img = img/255.
    out = model.predict(np.expand_dims(img,0))
    return out
def grad_cam_generate(model,layer_name,nb_classes):
    index = tf.placeholder(dtype = tf.int16, shape = ())
    loss = tf.multiply(model.output , tf.one_hot([index],nb_classes))
    reduced_loss = tf.reduce_sum(loss[0])
    conv_output = [l for l in model.layers if l.name == layer_name][0].output
    grads = tf.gradients(reduced_loss,conv_output)[0]
    return conv_output,grads,index
def grad_cam(model,category_index,sess,images,*args):
    conv_output,grads,index = args[0]
    
    output , grads_val = sess.run([conv_output,grads],feed_dict = {model.input: np.expand_dims(images,0),
                                                                   index: category_index})
    weights = np.mean(grads_val,axis = (1,2))
    cams = np.sum(weights*output, axis =3)
  
    full_img = (images*255.)
  
    cams = np.maximum(cv2.resize(cams[0],(100,100)),0)
    heatmap = cams / np.max(cams)
    cams = cv2.applyColorMap(np.uint8(255 * heatmap), cv2.COLORMAP_JET)
    cams = np.float32(cams) + np.float32(full_img)
    cams = 255 * cams / np.max(cams)
    cams = np.uint8(cams)
  
    return cams,heatmap,np.uint8(full_img)
def test_vid(video, model,sess):
    """
    Argument:
        ___video: type is String. It can be "camera" or link video 
        ___model: type is Keras model. 
    """
    tmt_kind = ["red","red yellow", "green yellow","green","corrupt","nothing"]
    disp_size = (1366,768)
    i = 0
    a = 0
    arg = grad_cam_generate(model,"add_2",6)
    if video == "camera":
        cap = cv2.VideoCapture(0)
    elif video == "camera1":
        cap = cv2.VideoCapture(1)
    else:
        cap = cv2.VideoCapture(video)
    while(cap.isOpened()):
        _,frame = cap.read()
        img = cv2.resize(frame[40:410,140:500,:],(100,100))/255.
        start = time.time()
        predictions = model.predict(np.expand_dims(img,0))
        prob = np.max(predictions)
        predicted_class = np.argmax(predictions)
        print("     ",predicted_class)
        cam,heatmap,full_img = grad_cam(model, predicted_class,sess, img, arg)
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = np.concatenate((full_img,cam), axis = 1)
        img = cv2.resize(img,disp_size)
        end = time.time()
        fps = 1/(end - start)
        cv2.putText(img,tmt_kind[predicted_class]+":"+str(prob),(10,100),font,1.5,(255,255,0),2)
        cv2.putText(img,"fps:"+str(int(fps)),(10,200),font,1,(255,255,0),2)
        cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
        #screen = screeninfo.get_monitors()[0]
        cv2.moveWindow("Video", 0, 0)
        cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Video",img)
        key = cv2.waitKey(1)
        if(key == 27):#ESC key : 27
            break
    cap.release()
    cv2.destroyAllWindows()
    return 1


