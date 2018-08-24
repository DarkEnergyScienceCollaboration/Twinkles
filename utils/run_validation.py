import os
import sys
import matplotlib as mpl
mpl.rcParams['text.usetex'] = False
import matplotlib.pyplot as plt
from desc.twinkles import validate_ic

if __name__ == "__main__":

    cat_folder = sys.argv[1]

    visit_num = int(sys.argv[2])

    # The path to the directory, 'Dynamic'
    sne_SED_path = sys.argv[3]

    filter_list = ['u', 'g', 'r', 'i', 'z', 'y']

    print("Loading visit info")
    with open(os.path.join(cat_folder, 'phosim_cat_%i.txt' % visit_num)) as f:
        for line in f:
            line_info = line.split(' ')
            if line_info[0] == 'mjd':
                visit_mjd = float(line_info[1])
            elif line_info[0] == 'filter':
                visit_band = filter_list[int(line_info[1])]
            elif line_info[0] == 'vistime':
                delta_t = float(line_info[1])/2.

    # This converts the way phosim wants the time to opsim time
    visit_mjd -= delta_t/86400.0

    sne_SED_file_dir = 'Dynamic'

    print("Running tests")
    val_cat = validate_ic()
    
    df_gal, df_pt_src = val_cat.load_cat(cat_folder, visit_num)

    spr_agn = val_cat.process_sprinkled_agn(df_pt_src)

    agn_lens_gals = val_cat.process_agn_lenses(spr_agn, df_gal)
    
    agn_location_test = val_cat.compare_agn_location(spr_agn, agn_lens_gals)

    spr_sne = val_cat.process_sprinkled_sne(df_pt_src, sne_SED_file_dir)

    sne_lens_gals = val_cat.process_sne_lenses(df_gal)

    sne_location_test = val_cat.compare_sne_location(spr_sne, sne_lens_gals)

    test_agn_inputs = val_cat.compare_agn_inputs(spr_agn, agn_lens_gals)

    test_sne_lens_inputs = val_cat.compare_sne_lens_inputs(sne_lens_gals)

    test_sne_image_inputs = val_cat.compare_sne_image_inputs(spr_sne,
                                                             sne_lens_gals,
                                                             visit_mjd,
                                                             sne_SED_file_dir,
                                                             sne_SED_path)

    test_agn_lens_mags = val_cat.compare_agn_lens_mags(spr_agn, agn_lens_gals)

    test_sne_lens_mags = val_cat.compare_sne_lens_mags(sne_lens_gals)

    test_agn_image_mags = val_cat.compare_agn_image_mags(spr_agn, agn_lens_gals,
                                                         visit_mjd, visit_band)

    test_sne_image_mags = val_cat.compare_sne_image_mags(spr_sne, sne_lens_gals,
                                                         visit_mjd, visit_band)
