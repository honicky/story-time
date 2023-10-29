Generates a watercolor image children's image using the 
https://huggingface.co/ostris/watercolor_style_lora_sdxl LoRA

Pass in a json file to API:
```
{
  "prompt": "Your prompt here",
  "bucket_name": "the object storage bucket name in which to save the image",
  "object_key": "the object key for the image data"
}
```

So for example:
```
{
  "prompt": "Talia the little girl in a blue shirt and here golden retriever Noa go for a walk in the park",
  "bucket_name": "botos-generated-images",
  "image_id": "image-id-should-probably-be-a-uuid",
}
```

This upload generate the image and upload it to the object-storage location that you have specified.