'use client'
import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [canvasToken, setCanvasToken] = useState('');
  const [courses, setCourses] = useState([]);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await axios.post('http://localhost:8000/favorite-courses', { token: canvasToken });
      setCourses(response.data);
    } catch (error) {
      setError('Failed to fetch courses. Please check your Canvas token and try again.');
      console.error('Error fetching courses:', error);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-4xl font-bold mb-8">Canvas GPT</h1>
      <form onSubmit={handleSubmit} className="w-full max-w-md mb-8">
        <input
          type="text"
          value={canvasToken}
          onChange={(e) => setCanvasToken(e.target.value)}
          placeholder="Enter your Canvas Access Token"
          className="w-full px-3 py-2 border border-gray-300 rounded-md mb-4"
          required
        />
        <button 
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600"
        >
          Fetch Favorite Courses
        </button>
      </form>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      {courses.length > 0 && (
        <div className="w-full max-w-2xl">
          <h2 className="text-2xl font-bold mb-4">Your Favorite Courses</h2>
          {courses.map((course) => (
            <div key={course.id} className="mb-4 p-4 border border-gray-300 rounded-md">
              <h3 className="text-xl font-semibold">{course.name}</h3>
              <p>{course.summary}</p>
            </div>
          ))}
        </div>
      )}
    </main>
  )
}