import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const { all_courses } = req.query;
    const response = await axios.get(`http://localhost:8000/courses${all_courses ? '?all_courses=true' : ''}`);
    res.status(200).json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching courses' });
  }
}