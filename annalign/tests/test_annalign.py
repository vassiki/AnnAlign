import annalign
import numpy as np
import numpy.testing as npt


def r_over_list(in_array, tr):
    rounded = np.zeros(len(in_array))
    for i, val in enumerate(in_array):
        rounded[i] = annalign.downsample(val, tr)

    return rounded


def test_downsample():

    trs = np.arange(0.1, 1.0, 0.1)

    for tr in trs:
        # make sure same array is returned when array is made with the tr
        in_array = np.arange(0, 30, tr)
        down_array = r_over_list(in_array, tr)
        npt.assert_allclose(down_array, in_array, err_msg="Failed for resolution {}".format(tr))

    # run the test for a couple of trs I want to use!
    tr = 0.3
    vals = [0, 0.1, 0.3, 0.5, 1.0, 1.4, 1.7, 2.0, 2.5, 3.2, 3.6, 4.0]
    tr_3_vals = [0, 0, 0.3, 0.6, 0.9, 1.5, 1.8, 2.1, 2.4, 3.3, 3.6, 3.9]
    out_0_3_array = r_over_list(vals, tr)
    npt.assert_allclose(tr_3_vals, out_0_3_array, err_msg="Failed to create intended output for 0.3")

    tr = 0.5
    tr_5_vals = [0, 0, 0.5, 0.5, 1.0, 1.5, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    out_0_5_array = r_over_list(vals, tr)
    npt.assert_allclose(tr_5_vals, out_0_5_array, err_msg="Failed to create intended output for 0.5")

    tr = 1.0
    tr_1_vals = [0, 0, 0, 0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 4.0, 4.0]
    out_1_array = r_over_list(vals, tr)
    npt.assert_allclose(tr_1_vals, out_1_array, err_msg="Failed to create intended output for 1.0")


    # just to be safe super high trs
    tr = 10.0
    tr_10_vals = np.zeros(len(vals))
    out_10_array = r_over_list(vals, tr)

    npt.assert_allclose(tr_10_vals, out_10_array, err_msg="Failed to create intended output for 10.0")

# write a test function that has known time stamps, such that time stamps dissapear with increasing tr
test_downsample()


