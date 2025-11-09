# TUV-batch-python: Comprehensive Documentation

**Author:** Fanghe Zhao
**Version:** Based on TUV 5.3.2
**Last Updated:** 2025-11-09

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Background: The TUV Model](#2-background-the-tuv-model)
3. [Installation and Requirements](#3-installation-and-requirements)
4. [Project Architecture](#4-project-architecture)
5. [Getting Started](#5-getting-started)
6. [API Reference](#6-api-reference)
7. [Data Files and Structure](#7-data-files-and-structure)
8. [Technical Details](#8-technical-details)
9. [Advanced Usage](#9-advanced-usage)
10. [Troubleshooting](#10-troubleshooting)
11. [Contributing](#11-contributing)
12. [References and Citations](#12-references-and-citations)

---

## 1. Project Overview

### 1.1 Purpose

TUV-batch-python is a Python wrapper that enables batch execution of the Tropospheric Ultraviolet-Visible (TUV) radiation model. This project provides a programmatic interface to run TUV simulations from Python scripts, making it easier to integrate photolysis rate calculations into larger atmospheric chemistry workflows.

### 1.2 Key Features

- **Batch Processing:** Run multiple TUV simulations with different parameters programmatically
- **Python Integration:** Simple Python API for incorporating TUV into existing Python workflows
- **Automated Compilation:** Automatically compiles Fortran source code on first run
- **Photolysis Rate Extraction:** Automatically parses and extracts photolysis rates for key atmospheric species
- **Flexible Parameters:** Control solar zenith angle, altitude, and temperature for each simulation

### 1.3 Use Cases

- Atmospheric chemistry modeling
- Photochemical box model simulations
- Air quality modeling
- Climate chemistry studies
- Research requiring photolysis rate calculations

---

## 2. Background: The TUV Model

### 2.1 What is TUV?

The Tropospheric Ultraviolet-Visible (TUV) radiation model is a comprehensive tool for calculating:

- **Spectral actinic flux** in the Earth's atmosphere
- **Spectral irradiance** at the surface and throughout the atmosphere
- **Photolysis rate coefficients** (J-values) for atmospheric photochemical reactions
- **UV radiation doses** relevant to biological systems

### 2.2 TUV Scientific Background

TUV was developed by Sasha Madronich and collaborators at the National Center for Atmospheric Research (NCAR). The model solves the radiative transfer equation considering:

- **Solar radiation:** Extraterrestrial solar spectrum
- **Atmospheric gases:** Ozone (O₃), oxygen (O₂), nitrogen dioxide (NO₂), sulfur dioxide (SO₂)
- **Atmospheric scattering:** Rayleigh scattering by air molecules
- **Aerosols:** Absorption and scattering by atmospheric particles
- **Clouds:** Impact on radiation transfer
- **Surface albedo:** Reflection from various surface types
- **Altitude effects:** Changes with height in the atmosphere

### 2.3 Version Information

This project uses **TUV Version 5.3.2** (June 2016) from NCAR, with modifications to support command-line batch processing.

### 2.4 Radiative Transfer Method

TUV employs sophisticated numerical methods:

- **Discrete Ordinates Method:** For accurate multi-stream radiative transfer
- **Two-Stream Approximation:** For faster calculations with pseudo-spherical correction
- **Spherical Geometry:** Accounts for Earth's curvature in slant path calculations

---

## 3. Installation and Requirements

### 3.1 System Requirements

**Operating System:**
- Linux (recommended)
- macOS (with compatible Fortran compiler)
- Windows (via WSL or Cygwin)

**Compiler:**
- gfortran (GNU Fortran compiler)
- Other Fortran compilers can be used by modifying the Makefile

**Python:**
- Python 3.x
- Required packages:
  - `more-itertools`
  - `numpy`

### 3.2 Installation Steps

#### Step 1: Clone the Repository

```bash
git clone https://github.com/your-repo/TUV-batch-python.git
cd TUV-batch-python
```

#### Step 2: Install Python Dependencies

```bash
pip install more-itertools numpy
```

#### Step 3: Verify Fortran Compiler

```bash
gfortran --version
```

If gfortran is not installed:

**Ubuntu/Debian:**
```bash
sudo apt-get install gfortran
```

**macOS (using Homebrew):**
```bash
brew install gcc
```

**CentOS/RHEL:**
```bash
sudo yum install gcc-gfortran
```

#### Step 4: Test Installation

```python
from tuv_api import tuv_cli

# First run compiles the Fortran code
SA = 60.0  # Solar zenith angle (degrees)
height = 0.0  # Altitude (km)
temperature = 298.0  # Temperature (K)
root_path = "./V5.3.2"  # Path to TUV source code

result = tuv_cli(SA, height, temperature, root_path)
if result == -1:
    print("Compilation completed. Run again.")
else:
    print("Photolysis rates:", result)
```

---

## 4. Project Architecture

### 4.1 Directory Structure

```
TUV-batch-python/
│
├── README.md                    # Basic project information
├── DOCUMENTATION.md             # This comprehensive documentation
├── tuv_api.py                   # Python wrapper/API
│
└── V5.3.2/                      # TUV Fortran source code
    ├── TUV.f                    # Main TUV program
    ├── Makefile                 # Build configuration
    ├── params                   # Parameter definitions
    │
    ├── *.f                      # TUV Fortran modules (30+ files)
    │   ├── functs.f             # Mathematical functions
    │   ├── grids.f              # Grid setup
    │   ├── orbit.f              # Solar orbit calculations
    │   ├── rdinp.f              # Input reading
    │   ├── rdxs.f               # Cross-section reading
    │   ├── rtrans.f             # Radiative transfer
    │   ├── rxn.f                # Reaction handling
    │   ├── qys.f                # Quantum yields
    │   ├── savout.f             # Output saving
    │   └── ...                  # Additional modules
    │
    └── DATAE1/                  # Data files directory
        ├── ATM/                 # Atmospheric profiles
        │   ├── ussa.ozone       # US Standard Atmosphere O₃
        │   ├── ussa.temp        # Temperature profile
        │   ├── ussa.dens        # Density profile
        │   └── ...
        │
        ├── GRIDS/               # Wavelength/altitude grids
        │   ├── combined.grid
        │   ├── fast_tuv.grid
        │   └── ...
        │
        ├── O3/                  # Ozone absorption cross-sections
        │   ├── 2006JPL_O3.txt
        │   ├── 1995Malicet_O3.txt
        │   └── ...
        │
        ├── O2/                  # Oxygen absorption data
        ├── NO2/                 # Nitrogen dioxide data
        ├── SO2/                 # Sulfur dioxide data
        ├── SUN/                 # Solar flux spectra
        │   ├── atlas3_1994_317_a.dat
        │   └── ...
        │
        └── Lakes_abs_store/     # Lake water absorption data
            └── *.csv            # Various lake measurements
```

### 4.2 Component Overview

#### Python Layer (tuv_api.py)

The Python API provides:
- Function wrapper for TUV execution
- Automatic compilation management
- Output parsing and extraction
- Data structure for photolysis rates

#### Fortran Core (V5.3.2/*.f)

The Fortran components handle:
- **TUV.f**: Main program and control flow
- **grids.f**: Wavelength and altitude grid setup
- **orbit.f**: Solar geometry calculations
- **rtrans.f**: Radiative transfer solver
- **rdxs.f**: Reading absorption cross-sections
- **rxn.f**: Photolysis reaction processing
- **qys.f**: Quantum yield calculations
- **savout.f**: Output generation

#### Data Files (DATAE1/)

Extensive spectroscopic and atmospheric data:
- Absorption cross-sections for atmospheric gases
- Solar irradiance spectra
- Atmospheric profile templates
- Quantum yield data
- Surface albedo specifications

---

## 5. Getting Started

### 5.1 Basic Usage Example

```python
from tuv_api import tuv_cli

# Define atmospheric conditions
solar_zenith_angle = 45.0  # degrees (0 = sun overhead)
altitude = 0.0             # km above sea level
temperature = 298.0        # K (25°C)
tuv_path = "./V5.3.2"      # Path to TUV directory

# Run TUV simulation
photolysis_rates = tuv_cli(
    solar_zenith_angle,
    altitude,
    temperature,
    tuv_path
)

# Check if compilation was needed
if photolysis_rates == -1:
    print("TUV compiled. Please run again.")
else:
    # Access photolysis rates
    print(f"O(1D) from O3: {photolysis_rates['o1d']:.2e} s⁻¹")
    print(f"NO2 photolysis: {photolysis_rates['no2']:.2e} s⁻¹")
    print(f"HCHO molecular: {photolysis_rates['hcho_m']:.2e} s⁻¹")
```

### 5.2 Running Multiple Simulations

```python
import numpy as np
from tuv_api import tuv_cli

# Set up parameter sweep
zenith_angles = np.arange(0, 90, 10)  # 0 to 85 degrees
altitudes = [0.0, 1.0, 2.0, 5.0]       # km
temperature = 298.0                     # K
tuv_path = "./V5.3.2"

results = []

for alt in altitudes:
    for sza in zenith_angles:
        rates = tuv_cli(sza, alt, temperature, tuv_path)
        if rates != -1:
            results.append({
                'sza': sza,
                'altitude': alt,
                'rates': rates
            })

# Analyze results
for result in results:
    print(f"SZA={result['sza']:5.1f}°, Alt={result['altitude']:4.1f}km: "
          f"NO2 J-value = {result['rates']['no2']:.2e} s⁻¹")
```

### 5.3 Integration with Atmospheric Models

```python
def calculate_photolysis_for_box_model(time_of_day, latitude, date, altitude, temp):
    """
    Calculate photolysis rates for a photochemical box model.

    Parameters:
    -----------
    time_of_day : float
        Hour of day (0-24)
    latitude : float
        Latitude in degrees
    date : tuple
        (year, month, day)
    altitude : float
        Altitude in km
    temp : float
        Temperature in K

    Returns:
    --------
    dict : Photolysis rate coefficients
    """
    from tuv_api import tuv_cli
    import solar_geometry  # hypothetical solar angle calculator

    # Calculate solar zenith angle
    sza = solar_geometry.calculate_sza(time_of_day, latitude, date)

    # Run TUV
    if sza < 90:  # Daytime
        j_values = tuv_cli(sza, altitude, temp, "./V5.3.2")
        return j_values if j_values != -1 else {}
    else:  # Night
        return {key: 0.0 for key in ['o1d', 'no2', 'hcho_m', ...]}
```

---

## 6. API Reference

### 6.1 Main Function: `tuv_cli()`

```python
tuv_cli(zenith_angle, height, temperature, root_path)
```

**Description:**
Wrapper function to execute the TUV radiation model and extract photolysis rate coefficients.

**Parameters:**

| Parameter | Type | Units | Description | Valid Range |
|-----------|------|-------|-------------|-------------|
| `zenith_angle` | float | degrees | Solar zenith angle (angle from vertical) | 0-90 |
| `height` | float | km | Altitude above sea level | 0-120 |
| `temperature` | float | K | Atmospheric temperature | 150-350 |
| `root_path` | str | - | Path to V5.3.2 directory | Valid path |

**Returns:**

- **dict**: Dictionary of photolysis rate coefficients (s⁻¹) for various species
- **int**: Returns `-1` on first run if compilation was needed

**Return Dictionary Keys:**

| Key | Description | Chemical Formula | Reaction |
|-----|-------------|------------------|----------|
| `o1d` | O(¹D) from ozone | O₃ → O(¹D) + O₂ | Primary oxidant |
| `no2` | Nitrogen dioxide | NO₂ → NO + O | NOₓ cycle |
| `no3_r` | Nitrate radical (path 1) | NO₃ → NO + O₂ | Nighttime chemistry |
| `no3_m` | Nitrate radical (path 2) | NO₃ → NO₂ + O | Nighttime chemistry |
| `hono` | Nitrous acid | HONO → OH + NO | OH source |
| `hono2` | Nitric acid | HNO₃ → OH + NO₂ | Nitrogen removal |
| `h2o2` | Hydrogen peroxide | H₂O₂ → 2OH | OH source |
| `ho2no2` | Peroxynitric acid | HO₂NO₂ → products | HOₓ-NOₓ coupling |
| `n2o5` | Dinitrogen pentoxide | N₂O₅ → products | NOₓ reservoir |
| `hcho_r` | Formaldehyde (radical) | HCHO → H + HCO | Radical channel |
| `hcho_m` | Formaldehyde (molecular) | HCHO → H₂ + CO | Molecular channel |
| `rooh` | Organic peroxide | ROOH → RO + OH | Organic oxidation |
| `acet_ro` | Acetaldehyde | CH₃CHO → products | VOC oxidation |
| `pan` | Peroxyacetyl nitrate | PAN → products | NOₓ reservoir |
| `meno3` | Methyl nitrate | CH₃ONO₂ → products | Organic nitrate |
| `etcome` | Methylethyl ketone | MEK → products | Ketone photolysis |
| `homecho` | Hydroxyacetaldehyde | HOCH₂CHO → products | Oxygenate |
| `glyxla` | Glyoxal (path a) | CHOCHO → products | Dicarbonyl |
| `glyxlb` | Glyoxal (path b) | CHOCHO → products | Dicarbonyl |
| `mecocho` | Methylglyoxal | CH₃COCHO → products | Dicarbonyl |
| `mecovi` | Methyl vinyl ketone | MVK → products | Isoprene oxidation |
| `macr` | Methacrolein | MACR → products | Isoprene oxidation |
| `biace` | Biacetyl | CH₃COCOCH₃ → products | Dicarbonyl |
| `afg1` | Additional factor | - | Reserved (set to 0.0) |

**Example:**

```python
from tuv_api import tuv_cli

rates = tuv_cli(
    zenith_angle=30.0,
    height=0.0,
    temperature=298.0,
    root_path="./V5.3.2"
)

if rates != -1:
    print(f"NO₂ photolysis rate: {rates['no2']:.3e} s⁻¹")
    print(f"O₃ → O(¹D) rate: {rates['o1d']:.3e} s⁻¹")
```

### 6.2 Understanding Photolysis Rates

**What are J-values?**

Photolysis rate coefficients (J-values) represent the first-order rate constant for photochemical reactions:

```
d[Species]/dt = -J × [Species]
```

Units: s⁻¹ (inverse seconds)

**Typical Ranges:**

- **Daytime (SZA < 60°)**: 10⁻⁶ to 10⁻² s⁻¹
- **Low sun (SZA 60-80°)**: 10⁻⁸ to 10⁻⁴ s⁻¹
- **Twilight (SZA > 80°)**: 10⁻¹⁰ to 10⁻⁶ s⁻¹
- **Nighttime**: ~0 s⁻¹

**Dependencies:**

J-values depend on:
1. Solar zenith angle (strongest factor)
2. Altitude (increases with height)
3. Ozone column (UV attenuation)
4. Clouds and aerosols (scattering/absorption)
5. Surface albedo (reflected radiation)

---

## 7. Data Files and Structure

### 7.1 Atmospheric Data (DATAE1/ATM/)

**US Standard Atmosphere Files:**

- `ussa.ozone`: Ozone concentration profile
- `ussa.temp`: Temperature vs. altitude
- `ussa.dens`: Air density profile
- `atmmod.afglmw.100`: AFGL midlatitude winter atmosphere
- `o3column.dat`: Total column ozone values
- `toms7.78_93.ave`: TOMS satellite ozone data

### 7.2 Spectroscopic Data

**Ozone Cross-sections (DATAE1/O3/):**
- `2006JPL_O3.txt`: JPL 2006 recommendation
- `1995Malicet_O3.txt`: Malicet et al. measurements
- `1986Molina.txt`: Molina & Molina data
- Temperature-dependent cross-sections

**Oxygen Data (DATAE1/O2/):**
- Schumann-Runge bands
- Herzberg continuum
- Lyman-Alpha absorption

**Nitrogen Dioxide (DATAE1/NO2/):**
- Temperature-dependent cross-sections
- Various spectroscopic databases

**Sulfur Dioxide (DATAE1/SO2/):**
- UV absorption data

### 7.3 Solar Irradiance (DATAE1/SUN/)

**Extraterrestrial Solar Spectra:**
- `atlas3_1994_317_a.dat`: ATLAS-3 space shuttle measurements
- `extsol.flx`: Composite solar spectrum
- Wavelength range: typically 121-850 nm

### 7.4 Grid Definitions (DATAE1/GRIDS/)

**Wavelength and Altitude Grids:**
- `combined.grid`: High-resolution combined grid
- `fast_tuv.grid`: Faster computation grid
- `isaksen.grid`: Isaksen chemistry grid
- `kockarts.grid`: Kockarts stratospheric grid

### 7.5 Lakes Absorption Data (DATAE1/Lakes_abs_store/)

Dissolved organic matter absorption data for various lakes:
- 100+ lake water absorption spectra
- CSV format with wavelength and absorption coefficient
- Used for aquatic photochemistry applications

---

## 8. Technical Details

### 8.1 Compilation Process

**Makefile Configuration:**

```makefile
FC = gfortran -static
FFLAGS = -Wno-argument-mismatch -O2
```

**Compilation Flags:**
- `-Wno-argument-mismatch`: Suppress Fortran argument warnings (gfortran 10+)
- `-O2`: Optimization level 2
- `-static`: Static linking (optional)

**Changing Compiler:**

To use a different Fortran compiler, edit `V5.3.2/Makefile`:

```makefile
# For Intel Fortran
FC = ifort
FFLAGS = -O2

# For PGI Fortran
FC = pgfortran
FFLAGS = -O2
```

### 8.2 Program Flow

1. **Python calls `tuv_cli()`**
   - Checks if `./tuv` executable exists
   - Compiles if needed (first run)

2. **Fortran TUV Execution**
   - Reads atmospheric profiles
   - Sets up wavelength/altitude grids
   - Loads absorption cross-sections
   - Calculates solar geometry
   - Solves radiative transfer equation
   - Computes photolysis rates
   - Outputs results to stdout

3. **Python parses output**
   - Captures stdout from TUV
   - Extracts photolysis rates
   - Returns structured dictionary

### 8.3 Output Parsing Details

The Python wrapper:
- Skips 19 header lines (lmmech = T setting)
- Reads 310 flux values
- Reads 313+ lines for reaction rates
- Reaction data in pairs: name, then rate
- Extracts specific reactions by index

**Output Format (from TUV stdout):**

```
[Header lines 1-19]
[Flux values lines 20-329]
[Blank lines]
[Reaction name]
[Reaction rate]
[Reaction name]
[Reaction rate]
...
```

### 8.4 Coordinate Systems and Units

**Angles:**
- Solar zenith angle: 0° (sun overhead) to 90° (horizon)
- Input in degrees, converted to radians internally

**Altitude:**
- Input: kilometers above sea level
- TUV internal: typically 0-120 km grid

**Temperature:**
- Input: Kelvin
- Affects absorption cross-sections
- Typical range: 200-320 K

**Wavelengths:**
- UV-B: 280-315 nm
- UV-A: 315-400 nm
- Visible: 400-700 nm
- TUV range: typically 121-850 nm

### 8.5 Numerical Methods

**Radiative Transfer:**
- Discrete ordinates method (DISORT)
- Pseudo-spherical correction for low sun
- Multiple scattering calculations

**Spectral Integration:**
- Photolysis rates integrated over wavelength:
  ```
  J = ∫ σ(λ) × φ(λ) × F(λ) dλ
  ```
  where:
  - σ(λ) = absorption cross-section
  - φ(λ) = quantum yield
  - F(λ) = actinic flux

---

## 9. Advanced Usage

### 9.1 Modifying TUV Parameters

For advanced users, you can modify TUV behavior by editing the Fortran source:

**Edit Input Parameters (V5.3.2/params):**

```fortran
* Maximum number of wavelength grid points
      INTEGER, PARAMETER :: kw = 700

* Maximum number of altitude levels
      INTEGER, PARAMETER :: kz = 151

* Maximum number of solar zenith angles
      INTEGER, PARAMETER :: kt = 50
```

**Recompile after changes:**
```bash
cd V5.3.2
make clean
make
```

### 9.2 Adding Custom Photolysis Reactions

To extract additional photolysis rates:

1. **Identify reaction index** in TUV output
2. **Edit `tuv_api.py`** to add new dictionary entry:

```python
output = {
    # ... existing entries ...
    "new_species": reaction_rate_tuv[INDEX],  # Add new species
}
```

### 9.3 Batch Processing Example

```python
import pandas as pd
from tuv_api import tuv_cli
import numpy as np

def batch_tuv_run(parameter_file, output_file):
    """
    Run TUV for multiple conditions from a CSV file.

    Input CSV columns: sza, altitude, temperature
    Output CSV: all input columns + all photolysis rates
    """
    # Read input parameters
    params = pd.read_csv(parameter_file)

    results = []
    tuv_path = "./V5.3.2"

    for idx, row in params.iterrows():
        print(f"Processing {idx+1}/{len(params)}...")

        rates = tuv_cli(
            row['sza'],
            row['altitude'],
            row['temperature'],
            tuv_path
        )

        if rates != -1:
            result_row = row.to_dict()
            result_row.update(rates)
            results.append(result_row)

    # Save results
    df_results = pd.DataFrame(results)
    df_results.to_csv(output_file, index=False)
    print(f"Saved results to {output_file}")

# Usage
batch_tuv_run('input_conditions.csv', 'photolysis_results.csv')
```

### 9.4 Visualization Example

```python
import matplotlib.pyplot as plt
import numpy as np
from tuv_api import tuv_cli

def plot_diurnal_variation(latitude=40, altitude=0, temp=298):
    """Plot diurnal variation of key photolysis rates."""

    # Solar zenith angles for full day
    # (simplified - real calculation needs date and solar geometry)
    sza_values = np.concatenate([
        np.linspace(85, 0, 30),    # Morning
        np.linspace(0, 85, 30)     # Afternoon
    ])

    j_no2 = []
    j_o1d = []
    j_hcho = []

    tuv_path = "./V5.3.2"

    for sza in sza_values:
        rates = tuv_cli(sza, altitude, temp, tuv_path)
        if rates != -1:
            j_no2.append(rates['no2'])
            j_o1d.append(rates['o1d'])
            j_hcho.append(rates['hcho_m'])

    # Create time axis (simplified)
    hours = np.linspace(6, 18, len(j_no2))

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(hours, j_no2, label='NO₂', linewidth=2)
    ax.plot(hours, j_o1d, label='O₃ → O(¹D)', linewidth=2)
    ax.plot(hours, j_hcho, label='HCHO', linewidth=2)

    ax.set_xlabel('Hour of Day', fontsize=12)
    ax.set_ylabel('J-value (s⁻¹)', fontsize=12)
    ax.set_yscale('log')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_title(f'Diurnal Photolysis Rates (Alt={altitude} km, T={temp} K)')

    plt.tight_layout()
    plt.savefig('diurnal_photolysis.png', dpi=300)
    plt.show()

# Run visualization
plot_diurnal_variation()
```

### 9.5 Sensitivity Analysis

```python
import numpy as np
from tuv_api import tuv_cli

def sensitivity_analysis():
    """Analyze sensitivity to temperature and altitude."""

    base_sza = 30.0
    tuv_path = "./V5.3.2"

    temperatures = np.linspace(270, 310, 5)  # K
    altitudes = np.linspace(0, 5, 6)         # km

    results = np.zeros((len(temperatures), len(altitudes)))

    for i, temp in enumerate(temperatures):
        for j, alt in enumerate(altitudes):
            rates = tuv_cli(base_sza, alt, temp, tuv_path)
            if rates != -1:
                results[i, j] = rates['no2']

    # Plot heatmap
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(results, aspect='auto', origin='lower',
                   extent=[altitudes[0], altitudes[-1],
                          temperatures[0], temperatures[-1]])
    ax.set_xlabel('Altitude (km)')
    ax.set_ylabel('Temperature (K)')
    ax.set_title(f'NO₂ J-value Sensitivity (SZA={base_sza}°)')
    plt.colorbar(im, label='J-value (s⁻¹)')
    plt.tight_layout()
    plt.savefig('sensitivity_analysis.png', dpi=300)
    plt.show()

sensitivity_analysis()
```

---

## 10. Troubleshooting

### 10.1 Common Issues and Solutions

#### Issue: Compilation Fails

**Error:** `gfortran: command not found`

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install gfortran

# macOS
brew install gcc

# Verify installation
gfortran --version
```

#### Issue: Argument Mismatch Warnings

**Error:** `Type mismatch in argument` or `Rank mismatch in argument`

**Solution:** Already handled in Makefile with `-Wno-argument-mismatch` flag. If using older gfortran:

```makefile
# For gfortran < 10
FFLAGS = -O2
```

#### Issue: Missing Python Packages

**Error:** `ModuleNotFoundError: No module named 'more_itertools'`

**Solution:**
```bash
pip install more-itertools numpy
```

#### Issue: Permission Denied

**Error:** `Permission denied: './tuv'`

**Solution:**
```bash
cd V5.3.2
chmod +x tuv
```

#### Issue: Wrong Output Format

**Error:** Photolysis rates are all zero or incorrect

**Possible Causes:**
1. Solar zenith angle > 90° (sun below horizon)
2. Wrong root_path specified
3. TUV input configuration changed

**Solution:**
- Verify SZA < 90° for daytime
- Check root_path points to V5.3.2 directory
- Ensure lmmech = T in TUV configuration

### 10.2 Debugging Tips

**Enable Verbose Output:**

Modify `tuv_api.py` to print TUV stdout:

```python
result = run(command_str, stdout=PIPE, stderr=None, shell=True, check=True)
stdout_text = result.stdout.decode("utf-8")
print(stdout_text)  # Add this line to see full output
```

**Check TUV Execution:**

Run TUV manually to test:

```bash
cd V5.3.2
./tuv 298.0 0.0 45.0  # temp height sza
```

**Verify Data Files:**

Ensure all data files exist:

```bash
ls V5.3.2/DATAE1/O3/
ls V5.3.2/DATAE1/SUN/
```

### 10.3 Performance Considerations

**Compilation Time:**
- First run: 10-30 seconds (compilation)
- Subsequent runs: < 1 second per simulation

**Memory Usage:**
- Typical: 10-50 MB per run
- Peak: ~100 MB for high-resolution grids

**Optimization:**
- For many runs, keep in same directory (avoid repeated path changes)
- Use compiled executable directly for maximum performance
- Consider parallelization for independent parameter sweeps

---

## 11. Contributing

### 11.1 How to Contribute

We welcome contributions to improve TUV-batch-python:

1. **Bug Reports:** Open an issue describing the problem
2. **Feature Requests:** Suggest new functionality
3. **Code Contributions:** Submit pull requests

### 11.2 Development Guidelines

**Code Style:**
- Follow PEP 8 for Python code
- Add docstrings to all functions
- Include type hints where applicable

**Testing:**
- Test with various SZA, altitude, temperature combinations
- Verify output format consistency
- Check edge cases (SZA near 90°, extreme temperatures)

**Documentation:**
- Update this documentation for new features
- Add examples for new functionality
- Comment complex algorithms

### 11.3 Reporting Issues

When reporting issues, include:
- Operating system and version
- Python version
- gfortran version
- Full error message
- Minimal code to reproduce the problem

---

## 12. References and Citations

### 12.1 TUV Model

**Primary Reference:**
> Madronich, S., and S. Flocke (1999), The role of solar radiation in atmospheric chemistry, in *Handbook of Environmental Chemistry*, edited by P. Boule, pp. 1-26, Springer-Verlag, Heidelberg.

**TUV Website:**
- NCAR TUV Model: https://www2.acom.ucar.edu/modeling/tropospheric-ultraviolet-and-visible-tuv-radiation-model

### 12.2 Radiative Transfer

**Discrete Ordinates Method:**
> Stamnes, K., S.-C. Tsay, W. Wiscombe, and K. Jayaweera (1988), Numerically stable algorithm for discrete-ordinate-method radiative transfer in multiple scattering and emitting layered media, *Appl. Opt.*, 27, 2502-2509.

### 12.3 Atmospheric Data

**US Standard Atmosphere:**
> U.S. Standard Atmosphere (1976), NOAA-S/T 76-1562, U.S. Government Printing Office, Washington, D.C.

**Ozone Absorption:**
> Molina, L. T., and M. J. Molina (1986), Absolute absorption cross sections of ozone in the 185- to 350-nm wavelength range, *J. Geophys. Res.*, 91, 14,501-14,508.

> Malicet, J., D. Daumont, J. Charbonnier, C. Parisse, A. Chakir, and J. Brion (1995), Ozone UV spectroscopy. II. Absorption cross-sections and temperature dependence, *J. Atmos. Chem.*, 21, 263-273.

**JPL Chemical Kinetics:**
> Sander, S. P., et al. (2006), Chemical Kinetics and Photochemical Data for Use in Atmospheric Studies, Evaluation Number 15, JPL Publication 06-2, Jet Propulsion Laboratory, Pasadena, CA.

### 12.4 Solar Irradiance

**ATLAS-3 Measurements:**
> VanHoosier, M. E., J.-D. F. Bartoe, G. E. Brueckner, and D. K. Prinz (1988), Absolute solar spectral irradiance 120 nm - 400 nm (Results from the Solar Ultraviolet Spectral Irradiance Monitor - SUSIM - Experiment on board Spacelab 2), *Astrophys. Lett. Commun.*, 27, 163-168.

### 12.5 License

**TUV License:**
- GNU General Public License v2.0 or later
- Copyright © 1994-2016 University Corporation for Atmospheric Research

**This Wrapper:**
- Developed by Fanghe Zhao
- Builds upon TUV 5.3.2 from NCAR

---

## Appendix A: Photochemistry Background

### A.1 Photolysis Fundamentals

Photolysis is the breaking of chemical bonds by absorption of light:

```
AB + hν → A + B
```

Where:
- AB = molecule
- hν = photon energy
- A, B = photoproducts

### A.2 Key Atmospheric Photolysis Reactions

**Ozone Photolysis:**
```
O₃ + hν → O₂ + O(¹D)     (λ < 320 nm)
O₃ + hν → O₂ + O(³P)     (λ < 1180 nm)
```
*Importance:* Source of hydroxyl radical (OH) via O(¹D) + H₂O

**NO₂ Photolysis:**
```
NO₂ + hν → NO + O(³P)    (λ < 420 nm)
```
*Importance:* Ozone formation via O(³P) + O₂

**Formaldehyde:**
```
HCHO + hν → H + HCO      (radical channel)
HCHO + hν → H₂ + CO      (molecular channel)
```
*Importance:* VOC oxidation, radical production

### A.3 Quantum Yields

The quantum yield (φ) is the fraction of absorbed photons that lead to a specific photochemical outcome:

```
φ = (number of product molecules) / (number of photons absorbed)
```

For multi-channel reactions:
```
Σ φᵢ ≤ 1
```

TUV incorporates temperature and wavelength-dependent quantum yields from laboratory studies.

---

## Appendix B: Quick Reference

### B.1 Function Call Template

```python
from tuv_api import tuv_cli

rates = tuv_cli(
    zenith_angle=FLOAT,   # 0-90 degrees
    height=FLOAT,         # km
    temperature=FLOAT,    # K
    root_path=STRING      # "./V5.3.2"
)
```

### B.2 Species Dictionary Keys

Quick reference for `rates` dictionary:

```
o1d, no2, no3_r, no3_m, hono, hono2, h2o2, ho2no2, n2o5,
hcho_r, hcho_m, rooh, acet_ro, pan, meno3, etcome, homecho,
glyxla, glyxlb, mecocho, mecovi, macr, biace, afg1
```

### B.3 Typical Values Reference

**NO₂ Photolysis (J-NO₂):**
- Noon, sea level, clear sky: ~8 × 10⁻³ s⁻¹
- Morning/evening (SZA 70°): ~1 × 10⁻³ s⁻¹
- Overcast: 50-70% of clear sky

**O₃ → O(¹D) (J-O¹D):**
- Noon, sea level: ~2 × 10⁻⁵ s⁻¹
- Morning/evening: ~1 × 10⁻⁶ s⁻¹

---

## Document Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-09 | Initial comprehensive documentation |

---

## Contact and Support

**Original TUV Model:**
- Sasha Madronich, NCAR/ACD
- Email: sasha@ucar.edu, tuv@acd.ucar.edu

**Python Wrapper:**
- Fanghe Zhao
- Repository: [TUV-batch-python](https://github.com/fzhao70/TUV-batch-python)

---

**End of Documentation**
