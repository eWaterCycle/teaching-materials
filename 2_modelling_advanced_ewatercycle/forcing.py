"""Forcing related functionality for HBV, see `eWaterCyle documentation <https://ewatercycle.readthedocs.io/en/latest/autoapi/ewatercycle/base/forcing/index.html>`_ for more detail."""
# Based on https://github.com/eWaterCycle/ewatercycle-marrmot/blob/main/src/ewatercycle_marrmot/forcing.py

from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
import xarray as xr
import numpy as np

from ewatercycle.base.forcing import DefaultForcing


RENAME_CAMELS = {'total_precipitation_sum':'pr',
                      'potential_evaporation_sum':'"evspsblpot"',
                      'streamflow':'Q'}

REQUIRED_PARAMS = ["pr", "evspsblpot"]
class HBVForcing(DefaultForcing):
    """Container for HBV forcing data.

    Args:
        camels_file: .txt file that contains CAMELS forcing from https://hess.copernicus.org/articles/21/5293/2017/
        pr: Path to a NetCDF (.nc) file containing precipitation - ensure yourself that these already match start_time & end time
        evspsblpot: Path to a NetCDF (.nc) file containing potential evaporation
        alpha: float provided in camels dataset but not in the forcing file, instead in the model results.
        test_data_bool: False by default, set True if instead of a camels file, a test files is passed for HBV including precipitation and evaporation contains columns: ["year", "month", "day", "pr", "evspsblpot"] seperated by a space

    Examples:

        From existing forcing data:

        .. code-block:: python

            from ewatercycle.forcing import sources

            forcing = sources.HBVForcing(
                directory='/home/davidhaasnoot/Code/Forcing/',
                start_time='1997-08-01T00:00:00Z',
                end_time='2000-08-31T00:00:00Z',
                camels_file='01620500_lump_cida_forcing_leap.txt',
                alpha = 1.20
            )

        Or provide forcing yourself as a NetCDF file

        .. code-block:: python

            forcing = sources.HBVForcing(
                directory='/home/davidhaasnoot/Code/Forcing/',
                start_time='1997-08-01T00:00:00Z',
                end_time='2000-08-31T00:00:00Z',
                pr="precipitation_file.nc"
                "evspsblpot"="potential_evaporation_file.nc"
            )

        where :py:const:`precipitation_file` &  :py:const:`potential_evaporation_file` can be the same aslong as
        they contain a  :py:const:`pr` &  :py:const:`evspsblpot` variable

        Inherited from base forcing:
            shape: Path to a shape file. Used for spatial selection.
            directory: Directory where forcing data files are stored.
            start_time: Start time of forcing in UTC and ISO format string e.g 'YYYY-MM-DDTHH:MM:SSZ'.
            end_time: End time of forcing in UTC and ISO format string e.g. 'YYYY-MM-DDTHH:MM:SSZ'.

    """

    # either a forcing file is supplied
    camels_file: Optional[str] = ".txt"
    # or pr and evspsblpot are supplied seperately - can also be the same dataset
    pr: Optional[str] = ".nc"
    evspsblpot: Optional[str] = ".nc"
    alpha: Optional[float] = 1.26 # varies per catchment, mostly 1.26?
    test_data_bool: bool = False # allows to use self.from_test_txt()

    # write_forcing_to_netcdf()

    # def write_forcing_to_netcdf(self)
    #     if self.test_data_bool:
    #        self.from_test_txt()
    #     elif wgliwrh

    #     self.evspsblpot.tonetCDF()
    #     write_yaml_thing()

    def camels_txt_defined(self):
        """test whether user defined forcing file, used converting text forcing file to netcdf"""
        if len(self.camels_file) > 4:
            return True
        else:
            return False

    def forcing_nc_defined(self):
        """test whether user defined forcing file"""
        if (len(self.pr) > 3) and (len(self.evspsblpot) > 3):
            return True
        else:
            return False

    def from_test_txt(self) -> xr.Dataset:
        """Load forcing data from a txt file into an xarray dataset.

        Information:
            Must contain ["year", "month", "day", "pr","Q", "evspsblpot"] in columns

            Will convert date to pandas.Timestamp()

            pr (precipitation), Q (discharge), evspsblpot (potential evaportaion) - all im mm's

        Returns:
            ds: xr.Dataset
                Dataset with forcing data.
        """
        if self.directory is None or self.camels_file is None:
            raise ValueError("Directory or camels_file is not set")
        fn = self.directory / self.camels_file
        forcing = np.loadtxt(fn, delimiter="	")
        names = ["year", "month", "day", "pr","Q", "evspsblpot"]
        df_in = pd.DataFrame(forcing, columns=names)
        df_in.index = df_in.apply(lambda x: pd.Timestamp(f'{int(x.year)}-{int(x.month)}-{int(x.day)}'), axis=1)
        df_in = df_in.drop(columns=["year", "month", "day"])
        df_in.index.name = "time"
        # TODO use netcdf-cf conventions
        ds = xr.Dataset(data_vars=df_in,
                        attrs={
                            "title": "HBV forcing data",
                            "history": "Created by ewatercycle_HBV.forcing.HBVForcing.to_xarray()",
                                },
                        )
        ds, ds_name = self.crop_ds(ds, "test")
        self.evspsblpot = ds_name
        self.pr = ds_name
        return ds

    def from_camels_txt(self) -> xr.Dataset:
        """Load forcing data from a txt file into an xarray dataset.

        Requirements:
            Must be in the same format as the CAMELS dataset:

            3 lines containing: lat, elevation and area.

            4th line with headers: 'Year Mnth Day Hr dayl(s) prcp(mm/day) srad(W/m2) swe(mm) tmax(C) tmin(C) vp(Pa)'

            Takes from the 5th line onwards with \t delimiter.

            Will convert date to pandas.Timestamp()

            Then convert from pandas to a xarray.

        Returns:
            ds: xr.Dataset
                Dataset with forcing data.
        """
        if self.directory is None or self.camels_file is None:
            raise ValueError("Directory or camels_file is not set")
        fn = self.directory / self.camels_file
        data = {}
        with open(fn, 'r') as fin:
            line_n = 0
            for line in fin:
                if line_n == 0:
                    data["lat"] = float(line.strip())
                elif line_n == 1:
                    data["elevation(m)"] = float(line.strip())
                elif line_n == 2:
                    data["area basin(m^2)"] = float(line.strip())
                elif line_n == 3:
                    header = line.strip()
                else:
                    break
                line_n += 1

        headers = header.split(' ')[3:]
        headers[0] = "YYYY MM DD HH"

        # read with pandas
        df = pd.read_csv(fn, skiprows=4, delimiter="\t", names=headers)
        df.index = df.apply(lambda x: pd.Timestamp(x["YYYY MM DD HH"][:-3]), axis=1)
        df = df.drop(columns="YYYY MM DD HH")
        df.index.name = "time"

        # rename
        new_names = [item.split('(')[0] for item in list(df.columns)]
        rename_dict = dict(zip(headers[1:], new_names))
        df.rename(columns=rename_dict, inplace=True)
        rename_dict2 = {'prcp': 'pr',
                        'tmax': 'tasmax',
                        'tmin': 'tasmin'}
        df.rename(columns=rename_dict2, inplace=True)

        # add attributes
        attrs = {"title": "HBV forcing data",
                 "history": "Created by ewatercycle_HBV.forcing.HBVForcing.from_camels_txt()",
                 "units": "daylight(s), precipitation(mm/day), mean radiation(W/m2), snow water equivalen(mm), temperature max(C), temperature min(C), vapour pressure(Pa)", }

        # add the data lines with catchment characteristics to the description
        attrs.update(data)

        ds = xr.Dataset(data_vars=df,
                        attrs=attrs,
                        )
        # Potential Evaporation conversion using srad & tasmin/maxs
        ds['evspsblpot'] = calc_pet(ds['srad'],
                             ds["tasmin"].values,
                             ds["tasmax"].values,
                             ds["time.dayofyear"].values,
                             self.alpha,
                             ds.attrs['elevation(m)'],
                             ds.attrs['lat']
                             )
        ds, ds_name= self.crop_ds(ds, "CAMELS")
        self.evspsblpot = ds_name
        self.pr = ds_name
        return ds

    def from_external_source(self):
        if None in [self.directory, self.pr, self.evspsblpot]:
            raise ValueError("Directory or camels_file is not set")

        # often same file
        if self.pr == self.evspsblpot:
            ds = xr.open_dataset(self.directory / self.pr)

            if sum([key in ds.data_vars for key in RENAME_CAMELS.keys()]) == len(RENAME_CAMELS):
                ds = ds.rename(RENAME_CAMELS)
                ds = ds.rename_dims({'date': 'time'})
                ds = ds.rename({'date': 'time'})

            ds, ds_name = self.crop_ds(ds, "external")
            self.evspsblpot = ds_name
            self.pr = ds_name
            return ds

        else:
            # but can also seperate
            ds_pr = xr.open_dataset(self.directory / self.pr)
            ds_evspsblpot = xr.open_dataset(self.directory / self.evspsblpot)
            combined_data_vars = list(ds_pr.data_vars) + list(ds_evspsblpot.data_vars)
            if not sum([param in combined_data_vars for param in REQUIRED_PARAMS]) == len(REQUIRED_PARAMS):
                raise UserWarning(f"Supplied NetCDF files must contain {REQUIRED_PARAMS} respectively")

            ds_pr, ds_name_pr = self.crop_ds(ds_pr, "external")
            self.pr = ds_name_pr

            ds_evspsblpot, ds_name_evspsblpot = self.crop_ds(ds_evspsblpot, "external")
            self.evspsblpot = ds_name_evspsblpot

            return ds_pr, ds_evspsblpot

    def crop_ds(self, ds: xr.Dataset, name: str):
        start = np.datetime64(self.start_time)
        end = np.datetime64(self.end_time)
        ds = ds.isel(time=(ds['time'].values >= start) & (ds['time'].values <= end))

        time = str(datetime.now())[:-10].replace(":", "_")
        # TODO maybe change this time aspect? can get quite large - or simply remove in finalize
        ds_name = f"HBV_forcing_{name}_{time}.nc"
        out_dir = self.directory / ds_name
        if not out_dir.exists():
            ds.to_netcdf(out_dir)

        return ds, ds_name

def calc_pet(s_rad, t_min, t_max, doy, alpha, elev, lat) -> np.ndarray:
    """Calculates Potential Evaporation using Priestly–Taylor PET estimate, callibrated with longterm P-T trends from the camels data set (alpha).

    Parameters:
        s_rad: np.ndarray
            net radiation estimate in W/m^2. Function converts this to J/m^2/d
        t_min: np.ndarray
            daily minimum temperature (degree C)
        t_max: np.ndarray
            daily maximum temperature (degree C)
        doy: np.ndarray
            day of year: use `xt.DataArray.dt.dayofyear` - used to approximate daylight amount
        alpha: float
            factor callibrated from longterm P-T trend compensating for lack of other data.
        elev: float
            elevation in m as provided by camels
        lat: float
            latitude in degree

    Assumptions:
        G = 0 in a day: no loss to ground.

    Returns:
        pet: np.ndarray
            Array containing PET estimates in mm/day

    Reference:
        based on code from:
                kratzert et al. 2022
                `NeuralHydrology --- A Python library for Deep Learning research in hydrology,
                Frederik Kratzert and Martin Gauch and Grey Nearing and Daniel Klotz <https://github.com/neuralhydrology/neuralhydrology/blob/master/neuralhydrology/datautils/pet.py>`_
                https://doi.org/10.21105/joss.04050
        Who base on `allen et al. (1998) 'FOA 56' <https://appgeodb.nancy.inra.fr/biljou/pdf/Allen_FAO1998.pdf>`_ & `Newman et al (2015) <https://hess.copernicus.org/articles/21/5293/2017/>`_

    """
    G = 0
    LAMBDA = 2.45  # MJ/kg

    s_rad = s_rad * 0.0864  # conversion Wm-2 -> MJm-2day-1
    albedo = 0.23  # planetary albedo
    in_sw_rad = (1 - albedo) * s_rad

    # solar declination
    sol_dec = 0.409 * np.sin((2 * np.pi) / 365 * doy - 1.39)  # Equation 24 FAO-56 Allen et al. (1998)

    # Sunset hour angle
    lat = lat * (np.pi / 180)  # degree to rad
    term = -np.tan(lat) * np.tan(sol_dec)
    term[term < -1] = -1
    term[term > 1] = 1
    sha = np.arccos(term)

    # Inverse relative distance between Earth and Sun:
    ird = 1 + 0.033 * np.cos((2 * np.pi) / 365 * doy)  # Equation 23 FAO-56 Allen et al. (1998)

    # Extraterrestrial Radiation -  Equation 21 FAO-56 Allen et al. (1998)
    et_rad = ((24 * 60) / np.pi * 0.082 * ird) * (
                sha * np.sin(lat) * np.sin(sol_dec) + np.cos(lat) * np.cos(sol_dec) * np.sin(sha))

    # Clear sky radiation Equation 37 FAO-56 Allen et al. (1998)
    cs_rad = (0.75 + 2 * 10e-5 * elev) * et_rad

    # Actual vapor pressure estimated using min temperature - Equation 48 FAO-56 Allen et al. (1998
    avp = 0.611 * np.exp((17.27 * t_min) / (t_min + 237.3))

    # Net outgoing long wave radiation - Equation 49 FAO-56 Allen et al. (1998)
    term1 = ((t_max + 273.16) ** 4 + (t_min + 273.16) ** 4) / 2  # conversion in K in equation
    term2 = 0.34 - 0.14 * np.sqrt(avp)
    term3 = 1.35 * s_rad / cs_rad - 0.35
    stefan_boltzman = 4.903e-09
    out_lw_rad = stefan_boltzman * term1 * term2 * term3

    # psychrometer constant (kPa/C) - varies with altitude
    temp = (293.0 - 0.0065 * elev) / 293.0
    atm_pressure = np.power(temp, 5.26) * 101.3  # Equation 7 FAO-56 Allen et al. (1998)
    gamma = 0.000665 * atm_pressure

    # Slope of saturation vapour pressure curve Equation 13 FAO-56 Allen et al. (1998)
    t_mean = 0.5 * (t_min + t_max)
    s = 4098 * (0.6108 * np.exp((17.27 * t_mean) / (t_mean + 237.3))) / ((t_mean + 237.3) ** 2)

    rn = in_sw_rad - out_lw_rad
    pet = ((alpha / LAMBDA) * s * (rn - G)) / (s + gamma)
    return pet * 0.408  # energy to evap