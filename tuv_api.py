def tuv_cli(zenith_angle, height, temperature, root_path):
    """
    This function is a wrapper for TUV model.
    The function will run TUV model with given zenith angle, height, temperature.
    The function will return the photolysis rate of some species.
    
    """
    from more_itertools import chunked
    import os
    import numpy as np
    from subprocess import run, CalledProcessError, PIPE
    """
    Args:
        zenith_angle : [deg]
        temperature : [K]
        height : [km]
    """
    current_dir = os.getcwd()
    os.chdir(root_path)

    if not os.path.isfile("./tuv"):
        print("Compile at fist run, run again")
        run("make", stdout=None, stderr=None, shell = True, check = True)

        return -1

    command_str = "./tuv " + "  %6.3f"%temperature + "  %6.3f"%height + "  %6.3f"%zenith_angle
    result = run(command_str, stdout=PIPE, stderr=None, shell = True, check = True)
    result = [i.strip() for i in result.stdout.decode("utf-8").splitlines() if i]

    # Setting for lmmech = T
    result = result[19:] #skip header
    flux_list = result[:310]
    reation_list = result[313:]
    reaction_name_tuv = [item[0] for item in chunked(reation_list, 2)]
    reaction_rate_tuv = [float(item[1]) for item in chunked(reation_list, 2)]

    output = {
            "o1d"   : reaction_rate_tuv[1],
            "hcho_r": reaction_rate_tuv[17],
            "hcho_m": reaction_rate_tuv[18],
            "h2o2"  : reaction_rate_tuv[4],
            "hono"  : reaction_rate_tuv[11],
            "no2"   : reaction_rate_tuv[5],
            "no3_r" : reaction_rate_tuv[7],
            "no3_m" : reaction_rate_tuv[6],
            "rooh"  : reaction_rate_tuv[23],
            "hono2" : reaction_rate_tuv[12],
            "ho2no2": reaction_rate_tuv[13],
            "n2o5"  : reaction_rate_tuv[10],
            "acet_ro": reaction_rate_tuv[20], #CH3CHO
            "pan"   : reaction_rate_tuv[37],
            "etcome": reaction_rate_tuv[47],
            "meno3" : reaction_rate_tuv[25],
            "homecho": reaction_rate_tuv[45],
            "glyxla": reaction_rate_tuv[53],
            "glyxlb": reaction_rate_tuv[52],
            "mecocho": reaction_rate_tuv[54],
            "mecovi" : reaction_rate_tuv[42],
            "macr" : reaction_rate_tuv[42],
            "biace": reaction_rate_tuv[55],
            "afg1": 0.0
            }

    os.chdir(current_dir)
    return output

if __name__ == "__main__":
    SA = 60
    height = 0.0 #km
    temperature = 298.0 #K
    root_path = "/storage/border/storage-eas-p-yw22/personal/fzhao70/ML/TUVbatch-python/V5.3.2"
    print(tuv_cli(SA, height, temperature, root_path))

