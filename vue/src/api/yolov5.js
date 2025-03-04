import request from '@/utils/request.js'


export const detectImage = (yolov5)=>{
  return request.post('/yolov5/image', yolov5)
}

export const detectInstant = ()=>{
  return request.post('/yolov5/instant')
}
