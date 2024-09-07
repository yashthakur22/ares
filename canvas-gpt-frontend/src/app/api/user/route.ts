// src/app/api/user/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  try {
    console.log('Fetching user data from backend...');
    const response = await fetch('http://localhost:8000/user');
    const data = await response.json();
    console.log('Raw backend response:', data);
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error fetching user data:', error);
    return NextResponse.json({ error: 'An error occurred while fetching user data' }, { status: 500 });
  }
}