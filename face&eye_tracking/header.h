#include "opencv2/objdetect.hpp" 
#include "opencv2/highgui.hpp" 
#include "opencv2/imgproc.hpp" 
#include <iostream> 

using namespace std;
using namespace cv;

// Function for Face Detection 
void detectAndDraw(Mat& img, CascadeClassifier& cascade,
	CascadeClassifier& nestedCascade, double scale);
string cascadeName, nestedCascadeName;
