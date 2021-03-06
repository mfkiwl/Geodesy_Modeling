# Definition of InSAR-format data
# Write and output functions for the InSAR data format

import numpy as np
import matplotlib.pyplot as plt


def write_insar_invertible_format(InSAR_obj, unc_min, filename):
    # This function uses InSAR displacements to make an insar file that can be inverted.
    # Writes one header line and multiple data lines.
    # InSAR_obj is in mm, and written out is in meters
    print("Writing InSAR displacements into file %s " % filename);
    ofile = open(filename, 'w');
    ofile.write("# InSAR Displacements: Lon, Lat, disp(m), sigma, unitE, unitN, unitN \n");
    for i in range(len(InSAR_obj.lon)):
        if np.isnan(InSAR_obj.LOS[i]):
            continue;
        else:
            std = InSAR_obj.LOS_unc[i] * 0.001;  # in m
            if std < unc_min:
                std = unc_min;
            ofile.write('%f %f ' % (InSAR_obj.lon[i], InSAR_obj.lat[i]));
            ofile.write('%f %f ' % (0.001 * InSAR_obj.LOS[i], std));  # in m
            ofile.write('%f %f %f\n' % (InSAR_obj.lkv_E[i], InSAR_obj.lkv_N[i], InSAR_obj.lkv_U[i]));
        # Writing in meters
    ofile.close();
    return;


def plot_insar(txtfile, plotname, vmin=None, vmax=None):
    print("Plotting insar in file %s " % plotname);
    [lon, lat, disp] = np.loadtxt(txtfile, unpack=True, skiprows=1, usecols=(0, 1, 2));
    plt.figure(dpi=300, figsize=(8, 8));
    if vmin is not None:
        plt.scatter(lon, lat, c=disp, s=18, cmap='rainbow', vmin=vmin, vmax=vmax);
    else:
        plt.scatter(lon, lat, c=disp, s=18, cmap='rainbow');
    plt.colorbar();
    plt.title("InSAR with %d Points " % len(disp));
    plt.savefig(plotname);
    return;
