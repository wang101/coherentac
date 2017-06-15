class para
{      public:
            double lambda;//meter 
            double pix_size;//perimeter of each pixel
            int scr_size;//screen size
            double wave_number;//wavenumber = 1/lambda
            double distance;//distance from crystal to screen
            double epsilon;//parameter reserved for calculation of crystal
            char eulerdef[3]; //def of euler angle 'zxz' as default;
            int natom;//atom number
            bool magnetic_field;
           double magnetic_angle[3];
           double tesla;
           double miu;
           double temperature;
           para()
           {
  	eulerdef[0]='z';
            eulerdef[1]='x';
            eulerdef[2]='z';
            scr_size=129;
            pix_size=0.008645052112070126;
            distance=1.0;
            lambda = 1.00e-10;
            natom = 3395;
             magnetic_field = false;
             magnetic_angle[0] = 0;
             magnetic_angle[1] = 0;
             magnetic_angle[2] = 1;
             tesla = 1.0;
             miu = -9.274e-21;
            temperature = 273;
            }};