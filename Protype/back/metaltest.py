from PIL import Image
from metalmap import create_metallicmap
from _texturizing import image_to_seamless

def lora_text_to_image(prompt):
    import torch
    from diffusers import LCMScheduler, AutoPipelineForText2Image

    model_id = "Lykon/dreamshaper-7"
    adapter_id = "latent-consistency/lcm-lora-sdv1-5"

    pipe = AutoPipelineForText2Image.from_pretrained(model_id, torch_dtype=torch.float32)
    pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
    # pipe.to("cuda")

    # load and fuse lcm lora
    pipe.load_lora_weights(adapter_id)
    pipe.fuse_lora()


    # disable guidance_scale by passing 0
    imagen = pipe(prompt=prompt, num_inference_steps=4, guidance_scale=0).images[0]
    image = image_to_seamless(imagen, overlap = 0.1)
    image.show()
    return image

prompt = "Metall texture, high quality, plane image"
imagen = lora_text_to_image(prompt)

img = imagen
metallic_map = create_metallicmap(img)
metallic_map.show()