interface UserInfoProps {
    user: {
      name: string;
    };
  }
  
  export default function UserInfo({ user }: UserInfoProps) {
    return (
      <div className="bg-gray-100 p-4 rounded-lg mb-4">
        <h2 className="text-xl font-semibold">Welcome, {user.name}!</h2>
      </div>
    );
  }