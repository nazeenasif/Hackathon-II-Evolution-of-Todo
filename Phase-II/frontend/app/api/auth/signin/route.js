import { NextResponse } from 'next/server';

export async function POST(request) {
  try {
    const body = await request.json();

    // Forward the request to the backend
    const backendResponse = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/auth/signin`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    const responseData = await backendResponse.json();

    if (!backendResponse.ok) {
      return NextResponse.json(
        { message: responseData.detail || 'Signin failed' },
        { status: backendResponse.status }
      );
    }

    return NextResponse.json(responseData);
  } catch (error) {
    console.error('Signin error:', error);
    return NextResponse.json(
      { message: 'An error occurred during signin' },
      { status: 500 }
    );
  }
}