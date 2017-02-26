from data_2d import generator_2d, glob, sitk, Timer
from sklearn.model_selection import train_test_split

from keras.callbacks import EarlyStopping, TensorBoard
from keras.optimizers import RMSprop

from inception_resnet_v2 import create_inception_resnet_v2
from inception_v4 import create_inception_v4

SAMPLES_PER_EPOCH = 1000
INPUT_SHAPE = (299, 299)
PATCH_SIZE = 32
BATCH_SIZE = 32
NB_CLASSES = 4

print("Finding data ..."),
with Timer():
    image_filenames = glob('/Users/kasper/Data/OASIS/disc*/OAS1_*_MR1/PROCESSED/MPRAGE/T88_111/OAS1_*_MR1_mpr_n4_anon_111_t88_gfc.hdr')
    label_filenames = glob('/Users/kasper/Data/OASIS/disc*/OAS1_*_MR1/FSL_SEG/OAS1_*_MR1_mpr_n4_anon_111_t88_masked_gfc_fseg.hdr')

print('Loading %i images ...' % len(image_filenames)),
with Timer():
    images = [sitk.ReadImage(image_filename) for image_filename in image_filenames]
    labels = [sitk.ReadImage(label_filename) for label_filename in label_filenames]
    images_train, images_test, labels_train, labels_test = train_test_split(images, labels, train_size=0.66)

tensor_board = TensorBoard(log_dir='./TensorBoard')
early_stopping = EarlyStopping(monitor='acc', patience=2, verbose=1)

model = create_inception_v4((INPUT_SHAPE[0], INPUT_SHAPE[1], 1), nb_classes=NB_CLASSES, load_weights=False)
model.compile(optimizer=RMSprop(lr=0.045, rho=0.94, epsilon=1., decay=0.9), loss='categorical_crossentropy', metrics=['acc'])
model.fit_generator(generator_2d(images_train, labels_train, NB_CLASSES, INPUT_SHAPE, PATCH_SIZE, BATCH_SIZE), samples_per_epoch=SAMPLES_PER_EPOCH, nb_epoch=10, callbacks=[tensor_board, early_stopping], verbose=1)

