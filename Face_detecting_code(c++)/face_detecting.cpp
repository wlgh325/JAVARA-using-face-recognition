#include "header.h"


int main(int argc, char ** argv) {
	//얼굴 정면인식 haarcascade_frontalface_alt
	face_cascade_name = "C:\\opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_alt.xml";
	if ( !face_cascade.load(face_cascade_name) ) { 
		printf("--(!)Error loading face cascade\n"); 
		return -1; 
	}
	
	//웹캠 연결
	//영상 받아오기
	VideoCapture cam(0);
	Mat frame;

	cam.set(CV_CAP_PROP_FRAME_WIDTH, CAM_WIDTH);
	cam.set(CV_CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT);

	if (!cam.isOpened()) { 
		printf("--(!)Error opening video cam\n"); 
		return -1; 
	}


	//esc로 종료할때까지 웹캠으로 부터 계속 프레임을 받아옴
	while (cam.read(frame))
	{
		if (frame.empty())
		{
			printf(" --(!) No camd frame -- Break!");
			break;
		}

		detectAndDisplay(frame);	//매 프레임마다 얼굴 detecting
		char c = (char)waitKey(10);
		if (c == 27) { break; }
	}
	return 0;
}

/** @function detectAndDisplay */
void detectAndDisplay(Mat frame)
{
	std::vector<Rect> faces;
	Mat frame_gray;

	cvtColor(frame, frame_gray, COLOR_BGR2GRAY);
	equalizeHist(frame_gray, frame_gray);

	//face detecting 
	/*void CascadeClassifier::detectMultiScale(const Mat& image, vector<Rect>& objects, 
		double scaleFactor = 1.1, int minNeighbors = 3,
		int flags = 0, Size minSize = Size(), Size maxSize = Size()) */
	// min , max size설정하면 일정 크기 이하나 이상의 얼굴 처리 No
	face_cascade.detectMultiScale(frame_gray, faces, 1.1, 2, 0 | CASCADE_SCALE_IMAGE, Size(30, 30));

	//검출한 얼굴을 전부 주황색의 원 모양으로 표시
	for (size_t i = 0; i < faces.size(); i++)
	{
		Point center(faces[i].x + faces[i].width / 2, faces[i].y + faces[i].height / 2);
		ellipse(frame, center, Size(faces[i].width / 2, faces[i].height / 2),
			0, 0, 360, Scalar(0, 0, 255), 4, 8, 0);
	}

	//window를 띄워서 결과 보여주기
	imshow(window_name, frame);
}


