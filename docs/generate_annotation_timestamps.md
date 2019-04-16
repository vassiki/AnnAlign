In the folder that you just cloned with `https://github.com/vassiki/annalign.git`, create an `annotations`
folder. Within the `annotations` folder, create `eaf` and `raw` folders.

The `raw` folder should contain txt files with the annotation timestamps

In order to generate the actual timing files, you should first launch `ipython`. Then, you can 
follow the steps listed here

- [ ] Import the module

```
import oneD
``` 

- [ ] Create a temporary dataframe that's holds the file you are interested in

```
filename = #file that exists under ../annotations/raw
df = oneD.format_file(filename)
```

- [ ] Provide information about the dimensions you are interested in, and the 
outputs should get saved in the appropriate location automatically!

```
oneD.timing_file(df, '01', 'Face Present')
```

The first argument is the dataframe you just created, the second is a string indicating the 
movie part (to make sure we don't overwrite files for different parts!) and the third
is name of the dimension you are interested in. You can choose any name for the dimension,
just make sure it is informative!

And then you're all set for the regression!
