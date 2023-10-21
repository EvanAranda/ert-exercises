#include <stdio.h>
#include <math.h>
#define MAX(x, y) (((x) > (y)) ? (x) : (y))

// gcc -lm test_j.c -o test_j

int main()
{
    double a = 0.0081;
    double b = 0.6;
    double g = 9.807;
    double pi = 4. * atan(1.);

    // ~0.1324739363
    double fptildemin = (1.0 / 2.0 / pi) * pow((4.0 * b / 5.0), (1.0 / 4.0));

    double gC = 5.87;
    double aC = 0.0317;

    double aX = (log(a) - log(aC)) / log(fptildemin);
    double gX = -log(gC) / log(fptildemin);

    double saC = 0.0547;
    double saX = 0.32;

    double sbC = 0.0783;
    double sbX = 0.16;

    double tmp0 = pow((2 * pi), -4) * pow(g, 2);

    double S, f, fp, fptilde;

    // loop 0 vars
    double fpt, alpha, gamma, sigma_a, sigma_b;

    // loop 1 vars
    double tmp1;

    // loop 2 vars
    double exp1arg, sigma, exp2arg;

    // loop 3 vars
    double tmp2, tmp3;

    for (fptilde = 0.; fptilde <= 10.; fptilde += 0.01)
    {
        fpt = MAX(fptilde, fptildemin);

        alpha = aC * pow(fpt, aX) * tmp0;
        gamma = gC * pow(fpt, gX);
        sigma_a = saC * pow(fpt, saX);
        sigma_b = sbC * pow(fpt, sbX);

        for (f = -5.; f <= 5.; f += 0.01)
        {
            tmp1 = alpha / (f * f * f * f * f);

            for (fp = 0.; fp <= 10.; fp += 0.01)
            {
                tmp2 = f / fp;
                tmp3 = (f - fp) / (sigma * fp);

                exp1arg = -1.25 / (tmp2 * tmp2 * tmp2 * tmp2);
                sigma = (f <= fp) * sigma_a + (f > fp) * sigma_b;
                exp2arg = -0.5 * tmp3 * tmp3;

                S = tmp1 * exp(exp1arg) * pow(gamma, exp(exp2arg));
            }
        }
    }
}
