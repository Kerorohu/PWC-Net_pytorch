import torch.nn as nn
import torch.nn.functional as F


from modules import (FeaturePyramidExtractor, WarpingLayer, CostVolumeLayer, OpticalFlowEstimator, ContextNetwork)




class Net(nn.Module):


    def __init__(self, args):
        super(Net, self).__init__()
        self.feature_pyramid_extractor = FeaturePyramidExtractor()
        self.warping_layer = WarpingLayer()
        self.cost_volume_layer = CostVolumeLayer()
        self.opticla_flow_estimator = OpticalFlowEstimator()
        self.context_network = ContextNetwork()
    

    def forward(self, src_img, tgt_img):
        print(src_img.size())
        # (B,3,H,W) -> (B,3,H/2,W/2) -> (B,3,H/4,W/4) -> (B,3,H/8,W/8)
        src_features = self.feature_pyramid_extractor(src_img)
        tgt_features = self.feature_pyramid_extractor(tgt_img)

        # on each level:
        # 1. upsample the flow on upper level
        # 2. warp tgt_feature
        # 3. build cost volume
        # 4. estimate flow
        flow = Variable(torch.zeros_like(src_features[-1]))
        for l in range(args.num_levels):
            flow_upsampled = F.upsample_bilinear(flow, scale_factor = 2)
            tgt_feature_warped = self.warping_layer(tgt_features[l], flow_upsampled)

            cost_volume = self.cost_volume_layer(src_features[l], tgt_feature_warped)

            flow = self.opticla_flow_estimator(src_features[l], cost_volume)
            final_flow, flow_pyramid = 0,0
        
        return flow_pyramid, None