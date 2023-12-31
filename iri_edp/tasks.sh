#!/bin/bash
set -e

USER_AGENT="User-Agent: Not a robot"

download_indices() {
    local output_dir="lib/iri16/indices"
    mkdir -p "$output_dir"
    curl "http://irimodel.org/indices/apf107.dat" -H "$USER_AGENT" --output-dir "$output_dir" -o "apf107.dat"
    curl "http://irimodel.org/indices/ig_rz.dat" -H "$USER_AGENT" --output-dir "$output_dir" -o "ig_rz.dat"
}

# download IRI-2016 model source code and data files
download_iri16() {
    mkdir -p "lib/iri16/src"
    mkdir -p "lib/iri16/common_files"

    curl "http://irimodel.org/IRI-2016/00_iri.tar" -H "$USER_AGENT" | tar -x -C "lib/iri16/src"
    curl "http://irimodel.org/COMMON_FILES/00_ccir-ursi.tar" -H "$USER_AGENT" | tar -x -C "lib/iri16/common_files"
    download_indices
}

build_iri_lib() {
    make -f iri16.makefile clean || true
    make -f iri16.makefile

    # copy the data files into the bin dir
    find lib/iri16/ \
        -type f \( -name "*.dat" -o -name "*.asc" \) \
        -exec cp {} bin/ \;
}

build_iri_edp() {
    make clean || true
    make
}

build() {
    build_iri_lib
    build_iri_edp
}

run() {
    pushd ./bin &>/dev/null
    trap "popd &> /dev/null" EXIT
    export LD_LIBRARY_PATH=.
    export DYLD_LIBRARY_PATH=.
    ./run_iri
}

# Create image of IRI parameters
# $1: x-axis label
# $2: x-axis column number
# $3: title
# $4: output file
plot() {
    now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    gnuplot <<-EOF
    set datafile separator ","
    set ylabel "Altitude (km)"
    set xlabel "$1"
    set title "$3 @ 37.8N, 75.4W\nGenerated by IRI-2016, $now"
    set style line 100 lt 1 lc rgb "grey" lw 0.5 
    set grid ls 100 
    set terminal png size 800,600
    set output "$4"
    plot "csv/t1.csv" u $2:1 w l tit "11:00 Mar 3, 2021", "csv/t2.csv" u $2:1 w l tit "23:00 Mar 4, 2021"
EOF
}

# Generates all 4 plots for each parameter of the iri struct (see src/run_iri.c).
plot_all() {
    mkdir -p plots
    plot "Plasma Frequency (MHz)" 2 "Electron Density Profile (EDP)" "plots/edp.png"
    plot "Temperature (k)" 3 "Neutral Temperature (Tn)" "plots/tn.png"
    plot "Temperature (k)" 4 "Ion Temperature (Ti)" "plots/ti.png"
    plot "Temperature (k)" 5 "Electron Temperature (Te)" "plots/te.png"
}

# Expands the script arguments to run one of the above commands
"$@"
