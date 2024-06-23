to run locally:

```py
# argument 1: the input image (defaults to "./image.png")
# arugment 2: the output image location and filename (defaults to "./updated.png")
# argument 3: the dot size (defaults to 10)
# argument 4: the image minimun width size (defaults to 2048)
# arugment 5: the shift of the halfttone (defaults to 2)
python halftone.py image.png updated.png 10 2048 2
```

![image](https://github.com/ethanjurman/halftone_effect/assets/1131494/11c2507c-903d-4e21-a7de-be368bcb1f0a)

You can change the shift (last parameter) to 0 to remove part of the halftone effect (this is most noticable around edges)
![image](https://github.com/ethanjurman/halftone_effect/assets/1131494/9b3e9c84-d821-4d07-b784-8e1e6a5cf29c)

You can change the dot size (in this example, it's set to 5 instead of 10)
![image](https://github.com/ethanjurman/halftone_effect/assets/1131494/a24c6923-2638-4537-9296-e99061896fe3)
