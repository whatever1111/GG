#include <iostream>
#include <cstdint>
#include <string>

#include <fstream>
#include <sstream>

#include <math.h>
#include <chrono>

#define M_PI 3.14159265358979323846

using namespace std;

void usage(){
  cerr<<"Usage: interpolateFloatImg inputImage outputImage kernelSize stdDeviation"<<endl;
}

/** Reads an image for the file inFile. Creates an array of the corect size in the heap.
 *  Returns true on success
 */
bool readImage(float * &image, const char * inFile, unsigned int &width, unsigned int &height){
  ifstream bIn;
  // fix the size of the two dimension variables to 32 bit
  uint32_t width32 = 0;
  uint32_t height32 = 0;
  
  // open the file for binary reading
  bIn.open(inFile, std::ofstream::in | std::ofstream::binary);
  if (!bIn.is_open()){
    cerr<<"Error opening file "<<inFile<<" for reading!"<<endl;
    return false;
  }

  // read the width and height
  bIn.read( (char*)&width32, sizeof(width32));
  bIn.read( (char*)&height32, sizeof(height32));
  // error checking
  if(width32 == 0 || height32 == 0){
    cerr<<"Width or height 0"<<endl;
    return false;
  }

  // setup the image
  width = width32;
  height = height32;
  image = new float[width * height];

  cout<<"Reading width "<<width<<" height  "<<height<<" = "<<width*height<<endl;

  // prepare reading the image
  float * imgInPtr = image;
  float * imgEndPtr = image + width * height;
  // read the input image
  while(bIn && imgInPtr != imgEndPtr){
    // actually read the data. Using a block copy might be faster - but it is quite fast anyways
    bIn.read((char*)imgInPtr++, sizeof(float));
  }
  return true;
}


/* writes the float array img to outFile (as binary floats, first 32bit width and height unsigned integers)
*/
bool writeImage(const float * img, const char * outFile, const unsigned int width, const unsigned int height){
  ofstream bOut;
  // open the file for writing
  bOut.open(outFile,  std::ofstream::binary);
  if (!bOut.is_open()){
    cerr<<"Error opening file "<<outFile<<" for writing!"<<endl;
    return false;
  }

  // write the width and height
  uint32_t width32 = width;
  uint32_t height32 = height;
  bOut.write((char*)&width32, sizeof(width32));
  bOut.write((char*)&height32, sizeof(height32));

  // write the data
  const float * imgPtr = img;
  const float * endPtr = img + (width*height);
  while(imgPtr != endPtr){
    bOut.write((const char*)imgPtr++, sizeof(float));
  }
  return true;
}

/** given the 2D kernel array of size size, it fills it with a 2D gaussian smoothing filter
 *  Returns true on success;
*/
bool createKernel(float * kernel, unsigned int size, double stdDeviation){

    int halfSize = size / 2;

    double r = 0;
		double goal = 0; //!!used
    double s = 2.0 * stdDeviation * stdDeviation; 
    double sum = 0.0;   // Initialization of sun for normalization
		double result = (M_PI * s); // !! cauculate it out of the recurrance
    for (int y = -halfSize; y <= halfSize; ++y) // Loop to generate 5x5 kernel
    {
        for(int x = -halfSize; x < y; ++x)
        {
            r = x*x + y*y;
						goal = (exp(-r / s)) / result; //!!calculate
            kernel[x + halfSize + (y + halfSize)*size] = goal;  //!!changed
						kernel[y + halfSize + (x + halfSize)*size] = goal;  //!!changed
            sum += 2 * goal;  //!!changed
        }
				r = y*y*2;
				goal = (exp(-r / s)) / result; //!!calculate
				kernel[(y + halfSize)*(size + 1)] = goal;  //!!changed
				sum += goal;  //!!changed
    }
 
		for (int i = 0; i < size; ++i) { // Loop to normalize the kernel
			for (int j = 0; j < i; ++j) {
				kernel[i + j*size] /= sum;
				kernel[j + i*size] /= sum; //!!changed
			}
			kernel[i + i*size] /= sum;  //!!changed
		}
  return true;
}

/** Given the input image, a coordinate therein, the width of the image, the kernel and the size of the kernel (one dimension),
 * this function returns:
 *   the smoothed image OR
 *   0.f (invalid) if more than 90% of the weighted input values are missing.
 */
float interpolateValue(const float * imgIn, const unsigned int xIn, const unsigned int yIn, const unsigned int width, const float * kernel, const unsigned int kernelSize){
  int halfSize = kernelSize / 2;
  float val = 0.f;
  float missingKernelVals = 0.f;
  // loop through the kernel
  for(int x = 0; x < kernelSize; ++x){
    for(int y = 0; y < x; ++y){  //!!
      // the value from the image
      float imgVal = imgIn[ xIn - halfSize + x  + (yIn - halfSize + y) * width];
      // the value from the kernel
      float kernelVal = kernel[ x + y * kernelSize];
      
      // check if the image value is valid
      if(imgVal != 0.f){
        val += imgVal * kernelVal;
      } else {
        missingKernelVals += kernelVal;
      }
			float imgVal = imgIn[yIn - halfSize + y + (xIn - halfSize + x) * width];
			float kernelVal = kernel[y + x * kernelSize];
			if (imgVal != 0.f) {
				val += imgVal * kernelVal;
			}
			else {
				missingKernelVals += kernelVal;
			}
    }
		float imgVal = imgIn[xIn - halfSize + x + (yIn - halfSize + x) * width];
		// the value from the kernel
		float kernelVal = kernel[x + x * kernelSize];

		// check if the image value is valid
		if (imgVal != 0.f) {
			val += imgVal * kernelVal;
		}
		else {
			missingKernelVals += kernelVal;
		}
  }
  // if we miss too much return 0.f
  if(missingKernelVals > 0.90) return 0.f;
  // return the calculated value with compensation for the missing values...
  return val / (1.f-missingKernelVals);
}

/** Interpolate the missing depth pixels in a depth image
 *  Given an input image and an output image, both with a certain width and height, apply the kernel (width kernelSize (one dimension)) to pixels
 *  which have the value 0.f
 *
 */
void interpolate(const float * imgIn, float * imgOut, const unsigned int &width, const unsigned int &height, const float *kernel, const unsigned int &kernelSize){

  int halfSize = kernelSize / 2;

  // go through all pixels
  for(int x = 0; x < width; ++x){
    for(int y = 0; y < height; ++y){
      // because of the size of the kernel we can not work on the edge of the depth image
      if(x >= halfSize && y >= halfSize && x < width-halfSize && y < height-halfSize){
        // check if this pixel is in fact unknown == 0
        if(imgIn[x + y*width] == 0.f){
          // this is an unknown pixel - interpolate it
          imgOut[x + y*width] = interpolateValue(imgIn, x, y, width, kernel, kernelSize);
        }else{
          // this pixel is valid - just copy it
          imgOut[x + y*width] = imgIn[x + y*width];
        }
      }
    }
  }
}


/** The main function. Five steps:
 *  1) check the program arguments
 *  2) create the Kernel
 *  3) read the input image
 *  4) interpolate
 *  5) write the output image
 *
 */
int main(int argc, char* argv[])
{
  // 1) check the program arguments
  if(argc != 5) {
    usage();
    return 0;
  }

  unsigned int kernelSize = 0;
  float stdDeviation = 0.f;
  // image dimensions
  unsigned int width = 0;
  unsigned int height = 0;
  

  kernelSize = atoi(argv[3]);
  stdDeviation = atof(argv[4]);

  if(kernelSize%2 == 0){
    cout<<"Kernel size must be odd!"<<endl;
    return 0;
  }

  cout<<"Kernel kernelSize  : "<<kernelSize<<endl;
  cout<<"Standard deviation : "<<stdDeviation<<endl;



  // 2) create the kernel
  float * kernel = new float[kernelSize*kernelSize];

  createKernel(kernel, kernelSize, stdDeviation);

  float * imgIn = 0;
  
  float min = 1.;
  float max = 0.;
  for(int x=0; x<kernelSize; ++x){
    for(int y=0; y<kernelSize; ++y){
      float val = kernel[x + y*kernelSize];
      if(val < min) min = val;
      if(val > max) max = val;
      //cout<<kernel[x + y*kernelSize]<<" ";
    }
    //cout<<endl;
  }
  cout<<"Kernel maximum: "<<max<<endl;
  cout<<"Kernel minimum: "<<min<<endl;



  // 3) read the image
  if(!readImage(imgIn, argv[1], width, height)){
    return 0;
  }

  float * imgOut = new float[width * height];

  std::chrono::high_resolution_clock::time_point start_time = chrono::high_resolution_clock::now();

  // 4) interpolate the image
  interpolate(imgIn, imgOut, width, height, kernel, kernelSize);

  std::chrono::high_resolution_clock::time_point end_time = chrono::high_resolution_clock::now();

  unsigned int microsecs = chrono::duration_cast<chrono::microseconds>(end_time - start_time).count();

  cout<<" Micro seconds: "<<microsecs<<endl;

  // 5) write the output
  writeImage(imgOut, argv[2], width, height);

  return 0;
}
