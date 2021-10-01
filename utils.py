import numpy as np
import torchio as tio
import torch
from skimage import measure
import scipy


def vol_dice_score(y_pred,y_true, smooth=1e-4):

    y_pred = y_pred.flatten()
    y_true = y_true.flatten()

    wp = 1

    tp = wp * ((y_pred * y_true).sum())
    fp = (y_pred * (1 - y_true)).sum()
    fn = ((1 - y_pred) * y_true).sum()

    return (2 * tp +smooth) / (2 * tp + fp + fn + smooth)

class ContourInPlaneAug(object):
    
    def __init__(self, w_spacing, h_spacing, w_stdMM,h_stdMM, angle, ob_type="random"): 
        '''
        w_spacing, h_spacing represents the spacing of the input image
        
        w_aMM, w_bMM are the measurements in MM; acts as the bound for variability along the in-plane directions
        
        angle - rotate Z such that ~ U(-angle,angle)
        
        ob_type specifies the bias types; can be either 'random' or 'systematic'
        '''
        
        
        self.w_spacing = w_spacing
        self.h_spacing = h_spacing
        
        self.w_stdMM = w_stdMM
        self.h_stdMM = h_stdMM
        self.angle = angle
        
        self.ob_type = ob_type
    
    def __call__(self, mask):  
        
        sys_type = np.random.choice(["inc","dec"]) #will only be considered if the bias type is systematic; 

        out_mask = torch.zeros_like(mask)
        
        z_indeces = [i.item() for i in torch.where(mask)[1].unique()] #To identify the slices where the ROI is present
        
        for z in z_indeces:
            
            if self.ob_type=="random":
                w_stdVOX = np.ceil(np.random.uniform(-self.w_stdMM,self.w_stdMM)/self.w_spacing) #conversion to equivalent voxels
                h_stdVOX = np.ceil(np.random.uniform(-self.h_stdMM,self.h_stdMM)/self.h_spacing)
                
            elif self.ob_type=="systematic":
                
                if sys_type == "inc":
                    w_stdVOX = np.ceil(np.random.uniform(0,self.w_stdMM)/self.w_spacing)
                    h_stdVOX = np.ceil(np.random.uniform(0,self.h_stdMM)/self.h_spacing)
                else:
                    w_stdVOX = np.ceil(np.random.uniform(-self.w_stdMM,0)/self.w_spacing)
                    h_stdVOX = np.ceil(np.random.uniform(-self.h_stdMM,0)/self.h_spacing)
            
            props = measure.regionprops(mask[0,z].data.numpy())
            w_min,h_min,w_max,h_max = props[0].bbox

            dw = w_max - w_min
            dh = h_max - h_min

            aug_dw = dw + w_stdVOX 
            aug_dh = dh + h_stdVOX 

            factor_w  = np.round(aug_dw/dw,2)
            factor_h = np.round(aug_dh/dh,2)
            
            if factor_w<=0:
                continue;
            
            if factor_h<=0:
                continue;
            
            scales = (1,1,factor_w,factor_w,factor_h,factor_h)#Z,Z,X,X,Y,Y
        
            degrees = (-self.angle, self.angle, 0, 0, 0, 0)#Z,X,X,Y,Y

            transform = tio.RandomAffine(scales=scales,degrees=degrees,p=1)

            out_mask[0,z] = transform(mask[0,z].unsqueeze(0).unsqueeze(0))[0,0]
            
           
        
        out_mask[out_mask>0.5] = 1
        out_mask[out_mask<=0.5] = 0
        
        
        return out_mask
    
 class ContourOutPlaneAug(object):
    
    def __init__(self, scale_a, scale_b,angle, delta_z):
        
        '''
        scale_a, scale_b and angle are transformation params and is only used when we synthesize masks beyond the GT boundaries
        
        delta_z is the maximum shift or out-plane augmentation allowed
        '''
        
        self.scale_a = scale_a
        self.scale_b = scale_b
        self.angle = angle
        
        self.delta_z = delta_z
        
    def __call__(self, mask):
        
        mask = mask.clone()
    
        aug_num_slices = np.random.randint(0, self.delta_z+1) #low, high (excluded high)
        
        z_indeces = [i.item() for i in torch.where(mask)[1].unique()]
        
        z_min, z_max = min(z_indeces), max(z_indeces)
        
        for i in range(aug_num_slices):
        
            dz = z_max-z_min

            if dz>0: 

                ref_z = np.random.choice([z_min,z_max])
                
                flag = -1 if ref_z==z_min else 1

                aug_type = "del" if np.random.uniform()>0.5 else "add"
            
                if mask[0,ref_z].sum()>0: #which means contour exists in that place, possible that it got deleted during iteration
                
                    if aug_type=="del":
                        if ref_z+flag in range(mask.shape[1]):
                            if mask[0,ref_z+flag].sum()==0:#to check if new contours were inserted up or down
                                mask[0,ref_z] = torch.zeros(*mask[0,ref_z].shape)
                                
                        else:#if ref_z+flag is outside the boundary
                            mask[0, ref_z] = torch.zeros(*mask[0,ref_z].shape)

                    elif aug_type=="add":

                        if ref_z+flag in range(mask.shape[1]):
                            
                            if mask[0,ref_z+flag].sum()==0:

                                scales =(1,1,self.scale_a,self.scale_b,self.scale_a,self.scale_b)
                                degrees = (-self.angle, self.angle,0,0,0,0)

                                transform = tio.RandomAffine(scales=scales,degrees=degrees,p=1)

                                mask[0,ref_z+flag] = transform(mask[0,ref_z].unsqueeze(0).unsqueeze(0))[0,0]

        mask[mask>0.5] = 1
        mask[mask<=0.5] = 0
        
        return mask
   
