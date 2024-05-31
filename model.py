import replicate

image = open("DSCF7791.jpg", "rb")

output = replicate.run(
    "tencentarc/gfpgan:297a243ce8643961d52f745f9b6c8c1bd96850a51c92be5f43628a0d3e08321a",
    input={
        "img": image,
        "scale": 2,
        "version": "v1.4"
    }
)
print(output)