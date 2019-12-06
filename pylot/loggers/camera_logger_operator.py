import erdust
import numpy as np
import os
import PIL.Image as Image

import pylot.utils


class CameraLoggerOperator(erdust.Operator):
    """ Logs camera frames."""

    def __init__(self, camera_stream, name, flags, filename_prefix):
        camera_stream.add_callback(self.on_frame)
        self._name = name
        self._flags = flags
        self._frame_cnt = 0
        self._filename_prefix = filename_prefix

    @staticmethod
    def connect(camera_stream):
        return []

    def on_frame(self, msg):
        self._frame_cnt += 1
        if self._frame_cnt % self._flags.log_every_nth_frame != 0:
            return
        # Write the image.
        if msg.encoding == 'BGR':
            frame = pylot.utils.bgr_to_rgb(msg.frame)
        elif msg.encoding == 'cityscapes':
            frame = msg.frame
        else:
            raise ValueError('{} unexpected frame encoding {}'.format(
                self._name, msg.encoding))
        file_name = os.path.join(
            self._flags.data_path,
            self._filename_prefix + str(msg.timestamp.coordinates[0]) + '.png')
        img = Image.fromarray(np.uint8(frame))
        img.save(file_name)