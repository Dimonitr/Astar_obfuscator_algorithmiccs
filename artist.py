import cv2
import numpy as np
from random import sample
from path_finding import AStar
import argparse

def astar_obfuscator(img, step=10, downsize_w_to=100, return_300x300=False):
  """
  Input:
    img : np.array         | Input image
    step : int [1,249]     | RGB thresholding step. The smaller it is the less intensive and detailed is the output image.
    dowsize_w_to : int     | The width of the image that goes to A*. The less it is the fatser the algorithm runs, but the less detailed output image size.
    return_300x300 : bool  | Whether to return the image of size (300,300) instead of the original size.
  Output:
    Image : np.array
  """
  org_h, org_w, org_c = img.shape
  downsize_h_to = org_h * downsize_w_to // org_w
  img = cv2.resize(img, (downsize_w_to,downsize_h_to), interpolation = cv2.INTER_AREA)
  paths = np.zeros_like(img)

  if return_300x300:
    org_h, org_w = 300, 300

  for ten in range(255,0,-step):
    for c in range(3):
      mask = (img[:,:,c]<=ten).astype(np.uint8)
      nonzero = np.nonzero(mask)

      if len(nonzero[0]) > 50:
        nonzero = list(zip(nonzero[0], nonzero[1]))
        mask = mask==0

        for h in range(100):   
          [src,dst] = sample(nonzero, 2)
          path = AStar(mask).search(src, dst)
          if path is not None:
            for p in path:
              paths[p[0],p[1],c] = ten-20
      else:
          return cv2.resize(paths, (org_w,org_h), interpolation = cv2.INTER_AREA)

  return cv2.resize(paths, (org_w,org_h), interpolation = cv2.INTER_AREA)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, required=True)
    parser.add_argument('--downscale', type=int, required=True)

    args = parser.parse_args()

    input_image = cv2.imread(args.image)
    out_image = astar_obfuscator(input_image, downsize_w_to=args.downscale)
    cv2.imwrite(args.image, out_image)