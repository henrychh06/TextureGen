from PIL import Image
from sanic import Sanic
from sanic.response import json
from sanic_ext import Extend
import io
import base64
import numpy as np
import os
import torch
import cv2
import utils.imgops as ops
import utils.architecture.architecture as arch
from diffusers import StableDiffusionPipeline
from bumpmapgen import BumpmapGenerator
from specmapgenerator import SpecularmapGenerator
from intensmap import IntensityMap
from intensBump import IntensityBumpMap
from _texturizing import image_to_seamless
from metalmap import create_metallicmap

app = Sanic("my-hello-world-app")
app.config.CORS_ORIGINS = ["http://localhost:3000", "http://3.87.69.168:3000"]

Extend(app)


def test_stable_diffusion_v1_5(prompt):
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, use_safetensors=True, variant="fp16", torch_dtype=torch.float16)
    pipe = pipe.to("cuda")
    pipe.enable_xformers_memory_efficient_attention()
    pipe.enable_model_cpu_offload()
    imagest = pipe(prompt).images[0]
    image = image_to_seamless(imagest, overlap=0.1)
    
    return image


def process(img, model):
    img = img * 1. / np.iinfo(img.dtype).max
    img = img[:, :, [2, 1, 0]]
    img = torch.from_numpy(np.transpose(img, (2, 0, 1))).float()
    img_LR = img.unsqueeze(0)
    img_LR = img_LR.to(device)
    output = model(img_LR).data.squeeze(0).float().cpu().clamp_(0, 1).numpy()
    output = output[[2, 1, 0], :, :]
    output = np.transpose(output, (1, 2, 0))
    output = (output * 255.).round()
    return output

def load_model(model_path):
    global device
    state_dict = torch.load(model_path)
    model = arch.RRDB_Net(3, 3, 32, 12, gc=32, upscale=1, norm_type=None, act_type='leakyrelu',
                          mode='CNA', res_scale=1, upsample_mode='upconv')
    model.load_state_dict(state_dict, strict=True)
    del state_dict
    model.eval()

    device = 'cpu'
    for k, v in model.named_parameters():
        v.requires_grad = False
    return model.to(device)


@app.get('/')
async def test(request):
    return json({'hello': 'world'})


@app.post('/upload')
async def upload(request):
    prompt = request.json.get("prompt", "")  # Obtener el prompt de la solicitud
    if not prompt:
        return json({'error': 'Prompt is required'}, status=400)

  
    generated_image = test_stable_diffusion_v1_5(prompt)
    
  
    image_np = np.array(generated_image)

    # (CPU o CUDA)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    
    path1 = ("utils/models/1x_FrankenMapGenerator-CX-Lite_215000_G.pth")
    OTHER_MAP_MODEL = path1
    path2 = ("utils/models/1x_NormalMapGenerator-CX-Lite_200000_G.pth")
    NORMAL_MAP_MODEL = path2
    models = [load_model(NORMAL_MAP_MODEL), load_model(OTHER_MAP_MODEL)]

    
    img_height, img_width = image_np.shape[:2]
    do_split = img_height > 512 or img_width > 512

    if do_split:
        rlts = ops.esrgan_launcher_split_merge(image_np, process, models, scale_factor=1, tile_size=512)
    else:
        rlts = [process(image_np, model) for model in models]

    normal_map = rlts[0]
    roughness = rlts[1][:, :, 1]
    displacement = rlts[1][:, :, 0]

    
    bump_generator = BumpmapGenerator(IntensityBumpMap.Mode.AVERAGE, 1.0, 1.0, 1.0, 0.0)
    bump_map = bump_generator.calculate_bumpmap(generated_image)

    
    spec_generator = SpecularmapGenerator(IntensityMap.Mode.AVERAGE, 1.0, 1.0, 1.0, 0.0)
    spec_map = spec_generator.calculate_specmap(generated_image, scale=1.5, contrast=1.0)

    metal_map = create_metallicmap(generated_image, contrast = 255)

    bump_map_np = np.array(bump_map)
    spec_map_np = np.array(spec_map)
    metal_map_np = np.array(metal_map)

    
    def convert_to_base64(img):
        _, buffer = cv2.imencode('.png', img)
        return base64.b64encode(buffer).decode('utf-8')

    response_data = {
        "base_image": convert_to_base64(image_np),
        "normal_map": convert_to_base64(normal_map),
        "roughness": convert_to_base64(roughness),
        "displacement": convert_to_base64(displacement),
        "bump_map": convert_to_base64(bump_map_np),
        "metal_map": convert_to_base64(metal_map_np)
    }

    return json(response_data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

