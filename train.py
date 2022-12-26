import tensorflow as tf
from object_detection.utils import config_util
from object_detection.protos import pipeline_pb2
from google.protobuf import text_format

# step 2 =======================


WORKSPACE_PATH = 'G:/ForPushGit/Sign-Language-Recognition/Tensorflow/workspace'
SCRIPTS_PATH = 'Tensorflow/scripts'
APIMODEL_PATH = 'Tensorflow/models'
ANNOTATION_PATH = WORKSPACE_PATH+'/annotations'
IMAGE_PATH = WORKSPACE_PATH+'/images'
MODEL_PATH = WORKSPACE_PATH+'/models'
PRETRAINED_MODEL_PATH = WORKSPACE_PATH+'/pre-trained-models'
#CONFIG_PATH = MODEL_PATH+'/my_ssd_mobnet/pipeline.config'
CHECKPOINT_PATH = MODEL_PATH+'/ssd_mobnet_ckp_alphabet/'

# step 2 =======================
CUSTOM_MODEL_NAME = 'ssd_mobnet_ckp_alphabet'
CONFIG_PATH = MODEL_PATH+'/'+CUSTOM_MODEL_NAME+'/pipeline.config'
config = config_util.get_configs_from_pipeline_file(CONFIG_PATH)



pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()
with tf.io.gfile.GFile(CONFIG_PATH, "r") as f:
    proto_str = f.read()
    text_format.Merge(proto_str, pipeline_config)
#
#
pipeline_config.model.ssd.num_classes = 25
pipeline_config.train_config.batch_size = 4
pipeline_config.train_config.fine_tune_checkpoint = PRETRAINED_MODEL_PATH+'/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/checkpoint/ckpt-0'
pipeline_config.train_config.fine_tune_checkpoint_type = "detection"
pipeline_config.train_input_reader.label_map_path= ANNOTATION_PATH + '/label_map2.pbtxt'
pipeline_config.train_input_reader.tf_record_input_reader.input_path[:] = [ANNOTATION_PATH + '/train_alpha.record']
pipeline_config.eval_input_reader[0].label_map_path = ANNOTATION_PATH + '/label_map2.pbtxt'
pipeline_config.eval_input_reader[0].tf_record_input_reader.input_path[:] = [ANNOTATION_PATH + '/test_alpha.record']

config_text = text_format.MessageToString(pipeline_config)
with tf.io.gfile.GFile(CONFIG_PATH, "wb") as f:
    f.write(config_text)

# step 2 =======================
# ===== step 1 =====
# labels = [{'name':'where', 'id':1},
#           {'name':'work', 'id':2},
#           {'name':'your', 'id':3},
#           {'name':'you', 'id':4},
#           {'name':'yes', 'id':5},]

# labels = [{'name':'b', 'id':1},
#           {'name':'c', 'id':2},]

# labels = [{'name':'ở đâu', 'id':1},
#           {'name':'làm', 'id':2},
#           {'name':'của bạn', 'id':3},
#           {'name':'bạn', 'id':4},
#           {'name':'có', 'id':5},]

# labels = [{'name':'nhà vệ sinh', 'id':1},
#           {'name':'đền từ', 'id':2},
#           {'name':'tạm biệt', 'id':3},
#           {'name':'xin chào', 'id':4},
#           {'name':'làm thế nào', 'id':5},
#           {'name':'bạn dạo này thế nào', 'id':6},
#           {'name':'tôi', 'id':7},
#           {'name':'anh yêu em', 'id':8},
#           {'name':'tôi ổn', 'id':9},
#           {'name':'đang học', 'id':10},
#           {'name':'nghĩa là gì', 'id':11},
#           {'name':'gặp bạn', 'id':12},
#           {'name':'của tôi', 'id':13},
#           {'name':'tên', 'id':14},
#           {'name':'rất vui được', 'id':15},
#           {'name':'không', 'id':16},
#           {'name':'ký hiệu', 'id':17},
#           {'name':'đánh vần', 'id':18},
#           {'name':'cảm ơn', 'id':19},
#           {'name':'giờ là mấy giờ thế', 'id':20},
#           {'name':'là gì', 'id':21},
#           {'name':'đâu', 'id':22},
#           {'name':'có', 'id':23},
#           {'name':'bạn', 'id':24},
#           {'name':'của bạn', 'id':25},]

# labels = [{'name':'a', 'id':1},
#           {'name':'b', 'id':2},
#           {'name':'c', 'id':3},
#           {'name':'d', 'id':4},
#           {'name':'đ', 'id':5},
#           {'name':'dm', 'id':6},
#           {'name':'dr', 'id':7},
#           {'name':'e', 'id':8},
#           {'name':'g', 'id':9},
#           {'name':'h', 'id':10},
#           {'name':'i', 'id':11},
#           {'name':'k', 'id':12},
#           {'name':'l', 'id':13},
#           {'name':'m', 'id':14},
#           {'name':'n', 'id':15},
#           {'name':'o', 'id':16},
#           {'name':'p', 'id':17},
#           {'name':'q', 'id':18},
#           {'name':'r', 'id':19},
#           {'name':'s', 'id':20},
#           {'name':'t', 'id':21},
#           {'name':'u', 'id':22},
#           {'name':'v', 'id':23},
#           {'name':'x', 'id':24},
#           {'name':'y', 'id':25},]

# labels = [{'name':'nhà vệ sinh', 'id':1},
#           {'name':'xin lỗi đã làm phiền', 'id':2},
#           {'name':'sở thích', 'id':3},
#           {'name':'từ đâu', 'id':4},
#           {'name':'tạm biệt', 'id':5},
#           {'name':'xin chào', 'id':6},
#           {'name':'này bạn ơi', 'id':7},
#           {'name':'làm thế nào', 'id':8},
#           {'name':'bạn dạo này thế nào', 'id':9},
#           {'name':'tôi', 'id':10},
#           {'name':'anh yêu em', 'id':11},
#           {'name':'tôi ổn', 'id':12},
#           {'name':'lại sau', 'id':13},
#           {'name':'đang học', 'id':14},
#           {'name':'của bạn', 'id':15},
#           {'name':'bạn', 'id':16},
#           {'name':'có', 'id':17},
#           {'name':'ở đâu', 'id':18},
#           {'name':'làm cái gì', 'id':19},
#           {'name':'cái gì', 'id':20},
#           {'name':'mấy giờ', 'id':21},
#           {'name':'cảm ơn', 'id':22},
#           {'name':'giữ sức khỏe', 'id':23},
#           {'name':'đánh vần', 'id':24},
#           {'name':'ký hiệu', 'id':25},
#           {'name':'hẹn gặp', 'id':26},
#           {'name':'làm ơn', 'id':27},
#           {'name':'không', 'id':28},
#           {'name':'rất vui', 'id':29},
#           {'name':'tên', 'id':30},
#           {'name':'của tôi', 'id':31},
#           {'name':'gặp bạn', 'id':32},
#           {'name':'ý nghĩa', 'id':33},
#           {'name':'thích', 'id':34},
#           {'name':'làm', 'id':35},]
#           {'name':'a', 'id':36},
#           {'name':'b', 'id':37},
#           {'name':'c', 'id':38},
#           {'name':'d', 'id':39},
#           {'name':'e', 'id':40},
#           {'name':'g', 'id':41},
#           {'name':'h', 'id':42},
#           {'name':'i', 'id':43},
#           {'name':'k', 'id':44},
#           {'name':'l', 'id':45},
#           {'name':'m', 'id':46},
#           {'name':'n', 'id':47},
#           {'name':'o', 'id':48},
#           {'name':'p', 'id':49},
#           {'name':'q', 'id':50},
#           {'name':'r', 'id':51},
#           {'name':'s', 'id':52},
#           {'name':'t', 'id':53},
#           {'name':'u', 'id':54},
#           {'name':'v', 'id':55},
#           {'name':'x', 'id':56},
#           {'name':'y', 'id':57},
#           {'name':'đ', 'id':58},]
# #
# with open(ANNOTATION_PATH + '\label_map2.pbtxt', 'w', encoding='utf-8') as f:
#     for label in labels:
#         f.write('item { \n')
#         f.write('\tname:\'{}\'\n'.format(label['name']))
#         f.write('\tid:{}\n'.format(label['id']))
#         f.write('}\n')

# ===== step 1 =====
print("smt")

# !python {SCRIPTS_PATH + '/generate_tfrecord.py'} -x {IMAGE_PATH + '/train'} -l {ANNOTATION_PATH + '/label_map.pbtxt'} -o {ANNOTATION_PATH + '/train.record'}
# !python {SCRIPTS_PATH + '/generate_tfrecord.py'} -x{IMAGE_PATH + '/test'} -l {ANNOTATION_PATH + '/label_map.pbtxt'} -o {ANNOTATION_PATH + '/test.record'}