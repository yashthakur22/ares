import { useState } from 'react';

interface Course {
  id: string;
  name: string;
  code: string;
  summary: string;
}

interface CourseListProps {
  courses: Course[];
}

export default function CourseList({ courses }: CourseListProps) {
  const [filter, setFilter] = useState('');

  const filteredCourses = courses.filter((course) =>
    course.name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <input
        type="text"
        placeholder="Filter courses..."
        className="w-full p-2 mb-4 border rounded"
        onChange={(e) => setFilter(e.target.value)}
      />
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredCourses.map((course) => (
          <div key={course.id} className="border p-4 rounded">
            <h3 className="text-xl font-semibold">{course.name}</h3>
            <p className="text-sm text-gray-600">{course.code}</p>
            <p className="mt-2">{course.summary}</p>
          </div>
        ))}
      </div>
    </div>
  );
}