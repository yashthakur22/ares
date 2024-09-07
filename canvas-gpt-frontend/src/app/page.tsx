"use client";

import { useState } from 'react';
import useSWR from 'swr';
import CourseList from '@/components/CourseList';
import UserInfo from '@/components/UserInfo';

const fetcher = async (url: string) => {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`An error occurred while fetching the data. Status: ${res.status}`);
  }
  return res.json();
};

export default function Home() {
  const [showAllCourses, setShowAllCourses] = useState(false);
  const { data: user, error: userError } = useSWR('/api/user', fetcher);
  const { data: courses, error: coursesError } = useSWR(
    () => `/api/courses${showAllCourses ? '?all_courses=true' : ''}`,
    fetcher
  );

  if (userError) return <div>Failed to load user: {userError.message}</div>;
  if (coursesError) return <div>Failed to load courses: {coursesError.message}</div>;
  if (!user) return <div>Loading user...</div>;
  if (!courses) return <div>Loading courses...</div>;

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Canvas GPT Dashboard</h1>
      <UserInfo user={user} />
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded mt-4"
        onClick={() => setShowAllCourses(!showAllCourses)}
      >
        {showAllCourses ? 'Show Favorite Courses' : 'Show All Courses'}
      </button>
      <CourseList courses={courses} />
    </main>
  );
}