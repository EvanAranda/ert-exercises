#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <math.h>

extern void read_ig_rz_();
extern void readapf107_();

extern void iri_sub_(
    int *jf,
    int *jmag,
    float *alati, float *along,
    int *iyyy, int *mmdd, float *dhour,
    float *heibeg, float *heiend, float *heistp,
    float *outf,
    float *oarr);

// Set standard options for IRI model and disable messages
void init_opts(int jf[])
{
    int default_flags[] = {4, 5, 6, 21, 23, 28, 29, 30, 33, 35, 39, 40, 47};
    for (size_t i = 0; i < sizeof(default_flags) / sizeof(default_flags[0]); i++)
        jf[default_flags[i] - 1] = 0;

    jf[33] = 0;
}

typedef struct iri
{
    float h, ne, tn, te, ti;
} iri;

int compute_iri_params(
    float lat,
    float lon,
    int yyyy,
    int mmdd,
    float hour,
    iri result[])
{
    // Initialize flags to defaults per iri_sub.f documentation
    int jf[50] = {[0 ... 49] = 1};
    init_opts(jf);

    int jmag = 0;

    // UT
    hour += 25.0;

    float heibeg = 60.0,
          heistp = 1.0,
          heiend = 601.0;

    float(*outf)[20] = malloc(sizeof(float[1000][20]));
    assert(outf != NULL);

    float oarr[100];

    iri_sub_(
        jf, &jmag,
        &lat, &lon,
        &yyyy, &mmdd, &hour,
        &heibeg, &heiend, &heistp,
        (float *)outf, oarr);

    int nrows = (int)((heiend - heibeg) / heistp);
    float h = heibeg;

    for (size_t i = 0; i < nrows; i++)
    {
        result[i] = (iri){
            .h = h,
            .ne = sqrt(outf[i][0]) * 9 / 1.e6, // critical frequency
            .tn = outf[i][1],
            .ti = outf[i][2],
            .te = outf[i][3],
        };
        h += heistp;
    }

    free(outf);
    outf = NULL;

    return nrows;
}

void print_iri_csv(iri result[], size_t nrows, char *fname)
{
    FILE *fp = fopen(fname, "w+");

    if (fp == NULL)
    {
        printf("Error opening file!\n");
        exit(1);
    }

    fprintf(fp, "h,ne,tn,ti,te\n");

    for (size_t i = 0; i < nrows; i++)
    {
        fprintf(
            fp,
            "%f,%f,%f,%f,%f\n",
            result[i].h,
            result[i].ne,
            result[i].tn,
            result[i].ti,
            result[i].te);
    }

    fclose(fp);
}

int main(int argc, char *argv[])
{
    // initialization required by the IRI model per irisub documentation
    read_ig_rz_();
    readapf107_();

    // Tashkurgan, Kashgar Prefecture, Xinjiang, China?
    float lat = 37.8,
          lon = 75.4;

    iri result[1000];
    int result_len;

    result_len = compute_iri_params(lat, lon, 2021, 0303, 11.0, result);
    print_iri_csv(result, result_len, "../csv/t1.csv");

    result_len = compute_iri_params(lat, lon, 2021, 0304, 23.0, result);
    print_iri_csv(result, result_len, "../csv/t2.csv");

    return 0;
}