from nyczone.geo.bbox import BBox

BOROUGH_BBOXES: dict[str, BBox] = {
    "manhattan": BBox(-74.0479, 40.6829, -73.9067, 40.8820),
    "brooklyn": BBox(-74.0421, 40.5707, -73.8334, 40.7395),
    "queens": BBox(-73.9626, 40.5431, -73.7004, 40.8007),
    "bronx": BBox(-73.9338, 40.7855, -73.7654, 40.9176),
    "statenisland": BBox(-74.2591, 40.4960, -74.0522, 40.6501),
}
