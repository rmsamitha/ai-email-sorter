import React, { useState, useEffect } from 'react';
import { GoogleLogin, GoogleOAuthProvider } from '@react-oauth/google';


// Simple SVG Icon Components
const MailIcon = () => (
  <svg className="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
  </svg>
);

const PlusIcon = () => (
  <svg className="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
  </svg>
);

const TrashIcon = () => (
  <svg className="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
  </svg>
);

const UserXIcon = () => (
  <svg className="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7a4 4 0 11-8 0 4 4 0 018 0zM9 14a6 6 0 00-6 6v1h12v-1a6 6 0 00-6-6zM21 12l-5 5m0-5l5 5" />
  </svg>
);

const CheckIcon = () => (
  <svg className="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
  </svg>
);

const SettingsIcon = () => (
  <svg className="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
  </svg>
);

const LogOutIcon = () => (
  <svg className="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
  </svg>
);

const InboxIcon = () => (
  <svg className="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
  </svg>
);

const ChevronRightIcon = () => (
  <svg className="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
  </svg>
);

const ArchiveIcon = () => (
  <svg className="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
  </svg>
);

const UserIcon = () => (
  <svg className="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
  </svg>
);

// Mock Auth Component
const LoginScreen = ({ onLogin }) => {
  const [email, setEmail] = useState('');

  const handleMockLogin = () => {
    if (email) {
      onLogin({
        email,
        name: email.split('@')[0],
        picture: `https://ui-avatars.com/api/?name=${email.split('@')[0]}&background=4F46E5&color=fff`
      });
    }
  };

  const handleGogleLoginSuccess = async (response) => {
    console.log('Login Success');
    console.log('Response:', response);
    
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    //const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
    
    if (!response.credential) {
      console.error('No credential in response');
      return;
    }
    
    if (!response.clientId) {
      console.error('VITE_GOOGLE_CLIENT_ID is not set in environment variables');
      return;
    }
    
    const body = JSON.stringify({
      credential: response.credential,
      client_id: response.clientId
    });

    console.log('Body:', body);
    // send the response to FastAPI's /google-auth endpoint
    fetch(`${apiUrl}/google-auth`, { 
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // Important: Include cookies in request
      body: body 
    })
    .then(response => {
      if (!response.ok) {
        return response.json().then(err => {
          throw new Error(JSON.stringify(err));
        });
      }
      return response.json();
    })
    .then(data => {
      console.log('Backend response:', data);
      // Handle successful authentication
      
      if (data.user) {
        // Store user data in localStorage for session persistence
        localStorage.setItem('user', JSON.stringify(data.user));
        
        // The JWT token is automatically stored in HttpOnly cookie by the browser
        // No need to manually store it - it will be sent with all requests automatically
        
        // Update app state to show authenticated user
        onLogin({
          email: data.user.email,
          name: data.user.name,
          picture: data.user.picture || `https://ui-avatars.com/api/?name=${data.user.name}&background=4F46E5&color=fff`
        });
      }
    }).then(data => {
      //handleGoogleConnect(); 
      //console.log('Redirected to Google OAuth login page=1');
    }).catch(error => {
      console.error('Error calling backend:', error);
    });
 
  };

const handleGoogleLoginFailure = (error) => {
  console.log('Login Failed');
  console.log(error);
};

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full">
        <div className="flex justify-center mb-6">
          <div className="w-16 h-16 bg-indigo-600 rounded-full flex items-center justify-center">
            <div className="w-8 h-8 text-white">
              <MailIcon />
            </div>
          </div>
        </div>
        <h1 className="text-3xl font-bold text-gray-900 text-center mb-2">AI Email Sorter</h1>
        <p className="text-gray-600 text-center mb-8">
          Automatically categorize and manage your emails with AI
        </p>

        <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID}>
            <GoogleLogin onSuccess={handleGogleLoginSuccess} onError={handleGoogleLoginFailure} />
        </GoogleOAuthProvider>
        

        <p className="text-xs text-gray-500 text-center mt-6">
          Mock login for development. Production will use Google OAuth.
        </p>
      </div>
    </div>
  );
};

// Header Component
const Header = ({ user, onSignOut }) => {
  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4 sticky top-0 z-10">
      <div className="flex items-center justify-between max-w-7xl mx-auto">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-indigo-600 rounded-full flex items-center justify-center">
            <div className="w-6 h-6 text-white">
              <MailIcon />
            </div>
          </div>
          <h1 className="text-2xl font-bold text-gray-900">AI Email Sorter</h1>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <img src={user.picture} alt={user.name} className="w-8 h-8 rounded-full" />
            <span className="text-sm text-gray-700 hidden sm:block">{user.email}</span>
          </div>
          <button
            onClick={onSignOut}
            className="flex items-center text-gray-600 hover:text-gray-900 transition"
            title="Sign Out"
          >
            <div className="w-5 h-5">
              <LogOutIcon />
            </div>
          </button>
        </div>
      </div>
    </header>
  );
};

// Connected Accounts Component
const ConnectedAccounts = ({ accounts, onAddAccount }) => {
  return (
    <section className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
      <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
        <div className="w-5 h-5 mr-2 text-indigo-600">
          <UserIcon />
        </div>
        Connected Accounts
      </h2>
      <div className="space-y-2">
        {accounts.map((account, idx) => (
          <div key={idx} className="flex items-center justify-between p-3 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border border-green-200">
            <div className="flex items-center space-x-3">
              <div className="w-5 h-5 text-green-600">
                <CheckIcon />
              </div>
              <span className="text-sm font-medium text-gray-900">{account.email}</span>
            </div>
            <span className="text-xs text-green-700 font-semibold px-2 py-1 bg-green-100 rounded-full">
              Connected
            </span>
          </div>
        ))}
      </div>
      <button
        onClick={onAddAccount}
        className="mt-4 flex items-center text-indigo-600 hover:text-indigo-700 text-sm font-medium transition"
      >
        <div className="w-4 h-4 mr-1">
          <PlusIcon />
        </div>
        Add another account
      </button>
    </section>
  );
};

// Category Form Component
const CategoryForm = ({ newCategory, onChange, onSubmit, onCancel }) => {
  return (
    <div className="mb-6 p-6 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl border border-indigo-200">
      <h3 className="font-semibold text-gray-900 mb-4 text-lg">Create New Category</h3>
      <div className="space-y-4">
        <input
          type="text"
          placeholder="Category name (e.g., Newsletters)"
          value={newCategory.name}
          onChange={(e) => onChange({ ...newCategory, name: e.target.value })}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
        />
        <textarea
          placeholder="Description (e.g., Marketing emails, newsletters, and promotional content)"
          value={newCategory.description}
          onChange={(e) => onChange({ ...newCategory, description: e.target.value })}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none resize-none"
          rows="4"
        />
        <div className="flex space-x-3">
          <button
            onClick={onSubmit}
            className="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition"
          >
            Create Category
          </button>
          <button
            onClick={onCancel}
            className="flex-1 px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

// Category Card Component
const CategoryCard = ({ category, onClick, onDelete }) => {
  return (
    <div
      className="border-2 border-gray-200 rounded-xl p-5 hover:border-indigo-400 hover:shadow-md cursor-pointer transition-all duration-200 bg-white"
      onClick={onClick}
    >
      <div className="flex items-start justify-between mb-3">
        <h3 className="font-semibold text-gray-900 text-lg">{category.name}</h3>
        <button
          onClick={(e) => { e.stopPropagation(); onDelete(); }}
          className="text-gray-400 hover:text-red-500 transition p-1 hover:bg-red-50 rounded"
        >
          <div className="w-4 h-4">
            <TrashIcon />
          </div>
        </button>
      </div>
      <p className="text-sm text-gray-600 mb-4 line-clamp-2">{category.description}</p>
      <div className="flex items-center justify-between pt-3 border-t border-gray-100">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center">
            <div className="w-4 h-4 text-indigo-600">
              <MailIcon />
            </div>
          </div>
          <span className="text-sm font-semibold text-gray-700">
            {category.emailCount || 0} emails
          </span>
        </div>
        <div className="w-5 h-5 text-gray-400">
          <ChevronRightIcon />
        </div>
      </div>
    </div>
  );
};

// Categories List Component
const CategoriesList = ({ categories, showForm, newCategory, onNewCategoryChange, onAddCategory, onCancelForm, onShowForm, onSelectCategory, onDeleteCategory }) => {
  return (
    <section className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-gray-900 flex items-center">
          <div className="w-5 h-5 mr-2 text-indigo-600">
            <InboxIcon />
          </div>
          Email Categories
        </h2>
        <button
          onClick={onShowForm}
          className="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition shadow-sm hover:shadow-md"
        >
          <div className="w-4 h-4 mr-2">
            <PlusIcon />
          </div>
          New Category
        </button>
      </div>

      {showForm && (
        <CategoryForm
          newCategory={newCategory}
          onChange={onNewCategoryChange}
          onSubmit={onAddCategory}
          onCancel={onCancelForm}
        />
      )}

      {categories.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {categories.map(category => (
            <CategoryCard
              key={category.id}
              category={category}
              onClick={() => onSelectCategory(category)}
              onDelete={() => onDeleteCategory(category.id)}
            />
          ))}
        </div>
      ) : (
        <div className="text-center py-16 bg-gray-50 rounded-xl">
          <div className="w-16 h-16 text-gray-300 mx-auto mb-4">
            <SettingsIcon />
          </div>
          <p className="text-gray-500 text-lg mb-2">No categories yet</p>
          <p className="text-gray-400 text-sm">Create your first category to start organizing emails</p>
        </div>
      )}
    </section>
  );
};

// Email Item Component
const EmailItem = ({ email, isSelected, onToggle, onClick }) => {
  const handleClick = (e) => {
    // Don't open modal if clicking checkbox
    if (e.target.type === 'checkbox') {
      e.stopPropagation();
      return;
    }
    onClick();
  };

  const handleCheckboxClick = (e) => {
    e.stopPropagation();
    onToggle();
  };

  return (
    <div
      onClick={handleClick}
      className={`bg-white rounded-xl shadow-sm p-5 transition-all duration-200 border-2 cursor-pointer ${isSelected ? 'border-indigo-500 shadow-md' : 'border-gray-200 hover:border-indigo-300 hover:shadow-md'
        }`}
    >
      <div className="flex items-start space-x-4">
        <input
          type="checkbox"
          checked={isSelected}
          onChange={handleCheckboxClick}
          onClick={handleCheckboxClick}
          className="w-5 h-5 mt-1 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-500 cursor-pointer"
        />
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between mb-2">
            <div className="flex-1 mr-4">
              <h3 className="text-sm font-semibold text-gray-900 mb-1 line-clamp-1">
                {email.subject}
              </h3>
              <p className="text-xs text-gray-600">From: {email.from}</p>
            </div>
            <div className="flex items-center space-x-2 flex-shrink-0">
              <div className="w-4 h-4 text-green-500">
                <ArchiveIcon />
              </div>
              <span className="text-xs text-gray-500 whitespace-nowrap">
                {new Date(email.receivedAt).toLocaleDateString()}
              </span>
            </div>
          </div>
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-4 mt-3 border border-blue-100">
            <p className="text-xs text-gray-700 leading-relaxed line-clamp-2">
              <span className="font-semibold text-indigo-700">AI Summary: </span>
              {email.summary}
            </p>
          </div>
        </div>
        <div className="w-5 h-5 text-gray-400 flex-shrink-0 mt-1">
          <ChevronRightIcon />
        </div>
      </div>
    </div>
  );
};

// Email Detail Page Component
const EmailDetailPage = ({ email, user, onBack, onDelete, onUnsubscribe, processing }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header user={user} onSignOut={() => { }} />

      <div className="max-w-5xl mx-auto p-6">
        {/* Back Button */}
        <button
          onClick={onBack}
          className="flex items-center text-gray-600 hover:text-gray-900 mb-6 transition"
        >
          <div className="w-5 h-5 transform rotate-180 mr-2">
            <ChevronRightIcon />
          </div>
          Back to Emails
        </button>

        {/* AI Summary Card */}
        <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-6 mb-6 border-2 border-indigo-200">
          <div className="flex items-start space-x-3">
            <div className="w-6 h-6 flex-shrink-0 mt-1 text-indigo-600">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div className="flex-1">
              <h3 className="text-sm font-bold text-indigo-900 mb-2 uppercase tracking-wide">AI Summary</h3>
              <p className="text-base text-gray-800 leading-relaxed">{email.summary}</p>
            </div>
          </div>
        </div>

        {/* Email Content Card */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          {/* Email Header */}
          <div className="border-b border-gray-200 p-6 bg-gray-50">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">{email.subject}</h1>

            <div className="space-y-3">
              <div className="flex items-start">
                <span className="text-sm font-semibold text-gray-500 w-24 flex-shrink-0">From:</span>
                <span className="text-sm text-gray-900 font-medium">{email.from}</span>
              </div>

              <div className="flex items-start">
                <span className="text-sm font-semibold text-gray-500 w-24 flex-shrink-0">Date:</span>
                <span className="text-sm text-gray-900">
                  {new Date(email.receivedAt).toLocaleString('en-US', {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </span>
              </div>

              {email.archived && (
                <div className="flex items-center space-x-2">
                  <span className="text-sm font-semibold text-gray-500 w-24 flex-shrink-0">Status:</span>
                  <div className="flex items-center space-x-2 text-green-600">
                    <div className="w-4 h-4">
                      <ArchiveIcon />
                    </div>
                    <span className="text-sm font-medium">Archived in Gmail</span>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Email Body */}
          <div className="p-6">
            <div className="prose prose-sm max-w-none">
              <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">{email.body}</p>
            </div>
          </div>

          {/* Actions Footer */}
          <div className="border-t border-gray-200 p-6 bg-gray-50 flex justify-end items-center space-x-3">
            <button
              onClick={onUnsubscribe}
              disabled={processing}
              className="flex items-center px-5 py-2.5 bg-orange-500 text-white rounded-lg font-semibold hover:bg-orange-600 transition disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md"
            >
              <div className="w-4 h-4 mr-2">
                <UserXIcon />
              </div>
              Unsubscribe
            </button>
            <button
              onClick={onDelete}
              disabled={processing}
              className="flex items-center px-5 py-2.5 bg-red-500 text-white rounded-lg font-semibold hover:bg-red-600 transition disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md"
            >
              <div className="w-4 h-4 mr-2">
                <TrashIcon />
              </div>
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Category View Component
const CategoryView = ({ category, emails, selectedEmails, onBack, onToggleEmail, onSelectAll, onBulkDelete, onBulkUnsubscribe, onEmailClick, processing }) => {
  const allSelected = emails.length > 0 && selectedEmails.length === emails.length;

  return (
    <div className="min-h-screen bg-gray-50">
      <Header user={{ picture: '', name: '', email: '' }} onSignOut={() => { }} />

      <div className="max-w-7xl mx-auto p-6">
        <div className="mb-6">
          <button
            onClick={onBack}
            className="flex items-center text-gray-600 hover:text-gray-900 mb-4 transition"
          >
            <div className="w-5 h-5 transform rotate-180 mr-2">
              <ChevronRightIcon />
            </div>
            Back to Categories
          </button>
          <h1 className="text-3xl font-bold text-gray-900">{category.name}</h1>
          <p className="text-gray-600 mt-2">{category.description}</p>
        </div>

        {emails.length > 0 ? (
          <>
            <div className="bg-white rounded-xl shadow-sm p-5 mb-6 border border-gray-200">
              <div className="flex items-center justify-between">
                <label className="flex items-center space-x-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={allSelected}
                    onChange={onSelectAll}
                    className="w-5 h-5 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-500 cursor-pointer"
                  />
                  <span className="text-sm font-medium text-gray-700">
                    {selectedEmails.length > 0
                      ? `${selectedEmails.length} of ${emails.length} selected`
                      : 'Select all'}
                  </span>
                </label>

                {selectedEmails.length > 0 && (
                  <div className="flex space-x-3">
                    <button
                      onClick={onBulkUnsubscribe}
                      disabled={processing}
                      className="flex items-center px-5 py-2 bg-orange-500 text-white rounded-lg font-semibold hover:bg-orange-600 transition disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md"
                    >
                      <div className="w-4 h-4 mr-2">
                        <UserXIcon />
                      </div>
                      Unsubscribe
                    </button>
                    <button
                      onClick={onBulkDelete}
                      disabled={processing}
                      className="flex items-center px-5 py-2 bg-red-500 text-white rounded-lg font-semibold hover:bg-red-600 transition disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md"
                    >
                      <div className="w-4 h-4 mr-2">
                        <TrashIcon />
                      </div>
                      Delete
                    </button>
                  </div>
                )}
              </div>
            </div>

            <div className="space-y-4">
              {emails.map(email => (
                <EmailItem
                  key={email.id}
                  email={email}
                  isSelected={selectedEmails.includes(email.id)}
                  onToggle={() => onToggleEmail(email.id)}
                  onClick={() => onEmailClick(email)}
                />
              ))}
            </div>
          </>
        ) : (
          <div className="bg-white rounded-xl shadow-sm p-16 text-center border border-gray-200">
            <div className="w-20 h-20 text-gray-300 mx-auto mb-4">
              <InboxIcon />
            </div>
            <p className="text-gray-500 text-lg">No emails in this category yet</p>
            <p className="text-gray-400 text-sm mt-2">New emails will appear here automatically</p>
          </div>
        )}
      </div>
    </div>
  );
};

// Demo Section Component
const DemoSection = ({ onSimulate, processing, categoriesExist }) => {
  if (!categoriesExist) return null;

  return (
    <section className="bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-xl p-6">
      <h3 className="font-semibold text-blue-900 mb-2 text-lg">Demo Mode</h3>
      <p className="text-sm text-blue-700 mb-4">
        Simulate receiving a new email to test the AI categorization
      </p>
      <button
        onClick={onSimulate}
        disabled={processing}
        className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md"
      >
        {processing ? 'Processing...' : 'Simulate New Email'}
      </button>
    </section>
  );
};

// Main App Component
export default function EmailSorterApp() {
  const [user, setUser] = useState(null);
  const [accounts, setAccounts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [emails, setEmails] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [showCategoryForm, setShowCategoryForm] = useState(false);
  const [newCategory, setNewCategory] = useState({ name: '', description: '' });
  const [selectedEmails, setSelectedEmails] = useState([]);
  const [processing, setProcessing] = useState(false);
  const [selectedEmailDetail, setSelectedEmailDetail] = useState(null);

  useEffect(() => {
    loadData();
    const checkSession = async () => {
      await verifySession(); // Wait for verifySession to complete
      console.log('verifySession() completed'); // Now this runs AFTER verifySession completes
      await fetchAndSetCategories();
      const savedUser = localStorage.getItem('user');
      if (savedUser) {
        const userData = JSON.parse(savedUser);
        // Call fetchInboxEmails after a short delay to ensure categories are fetched first
        //fetchInboxEmails(userData);
        processEmails(userData);
      }
    };
    checkSession();
    console.log('checkSession() completed');
    
    // Check if we're returning from OAuth callback
    const urlParams = new URLSearchParams(window.location.search);
    const oauthSuccess = urlParams.get('oauth_success');
    
    if (oauthSuccess === 'true') {
      console.log('OAuth callback detected - fetching categories and emails after redirect');
      // Clean up URL by removing the parameter
      const newUrl = window.location.pathname;
      window.history.replaceState({}, '', newUrl);
      
    } 
    
  }, []);

  // Fetch emails for the selected category
  useEffect(() => {
    console.log("in useEffect() >> selectedCategory changed: ", selectedCategory);
    
    
    
    //fetchEmailsForCategory();
  }, [selectedCategory]); // Only refetch when selectedCategory changes

  const loadData = () => {
    const savedUser = localStorage.getItem('user');
    const savedAccounts = localStorage.getItem('accounts');
    const savedCategories = localStorage.getItem('categories');
    const savedEmails = localStorage.getItem('emails');

    if (savedUser) setUser(JSON.parse(savedUser));
    if (savedAccounts) setAccounts(JSON.parse(savedAccounts));
    if (savedCategories) setCategories(JSON.parse(savedCategories));
    if (savedEmails) setEmails(JSON.parse(savedEmails));
  };

  // Call FastAPI resource auth/google/connect which returns authorization URL for Google OAuth
  // This function is used to initiate Gmail API OAuth flow
  const handleGoogleConnect = async () => {
    console.log('handleGoogleConnect() running');
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const response = await fetch(`${apiUrl}/auth/google/connect`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'Access-control-allow-origin': '*'
      },
    }); 
    console.log('Response from auth/google/connect:', response);
    if (response.ok) {
      const data = await response.json();
      if (data.authorization_url) {
        // Redirect user to Google OAuth consent screen
        window.location.href = data.authorization_url;
      } else {
        console.error('No authorization_url in response:', data);
      }
    } else {
      console.error('Error calling backend:', response.statusText);
    }
  };

  // Verify session with backend on page load
  const verifySession = async () => {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    
    try {
      // The cookie will be automatically sent with credentials: 'include'
      const response = await fetch(`${apiUrl}/me`, {
        method: 'GET',
        credentials: 'include', // Important: Include cookies in request
      });

      if (response.ok) {
        const userData = await response.json();
        // Session is valid, update user state
        const user = {
          email: userData.email,
          name: userData.name,
          picture: userData.picture
        };
        setUser(user);
        localStorage.setItem('user', JSON.stringify(user));
        
        // Fetch categories for authenticated user
        //fetchAndSetCategories();
        
        // Note: Gmail OAuth will be triggered automatically when user tries to fetch emails
        // and tokens are missing (handled in useEffect for selectedCategory)
      } else {
        // Session expired or invalid, clear local data
        if (response.status === 401) {
          setUser(null);
          localStorage.removeItem('user');
        }
      }
    } catch (error) {
      console.error('Session verification error:', error);
      // Don't clear user data on network errors
    }
  };

  const saveData = (key, data) => {
    localStorage.setItem(key, JSON.stringify(data));
  };

  // Fetch categories from backend API and update UI
  const fetchAndSetCategories = async () => {
    console.log('fetchAndSetCategories() running');
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    
    try {
      const response = await fetch(`${apiUrl}/categories`, {
        method: 'GET',
        credentials: 'include', // Important: Include cookies in request
      });

      if (response.ok) {
        const backendCategories = await response.json();
        
        // Transform backend categories to match frontend structure
        // Backend returns: { id: int, name, description, account_id }
        // Frontend expects: { id: string, name, description, emailCount }
        const transformedCategories = backendCategories.map(cat => {
          // Calculate emailCount from emails array
          const emailCount = emails.filter(e => e.categoryId === cat.id.toString()).length;
          
          return {
            id: cat.id.toString(), // Convert to string to match frontend
            name: cat.name,
            description: cat.description || '',
            emailCount: emailCount
          };
        });
        
        // Update state and localStorage
        setCategories(transformedCategories);
        saveData('categories', transformedCategories);
      } else {
        if (response.status === 401) {
          // User not authenticated
          console.error('Not authenticated to fetch categories');
        } else {
          console.error('Error fetching categories:', response.statusText);
        }
      }
    } catch (error) {
      console.error('Error fetching categories:', error);
      // Don't throw - allow app to continue with existing categories
    }
  };

  const handleLogin = (userData) => {
    setUser(userData);
    saveData('user', userData);

    // Don't call fetchAndSetCategories here because handleGoogleConnect redirects
    // It will be called after OAuth redirect completes (see useEffect above)
    handleGoogleConnect();
    console.log('Redirected to Google OAuth login page-ddd');
    // Note: fetchAndSetCategories() will be called after OAuth redirect completes
    
    // fetchInboxEmails() will also need to wait for OAuth completion
    // It should be called after OAuth redirect or when user explicitly requests it

    const newAccounts = [{ email: userData.email, connected: true }];
    setAccounts(newAccounts);
    
    // Note: Gmail OAuth will be triggered automatically when user tries to fetch emails
    // and tokens are missing (handled in useEffect for selectedCategory)
    saveData('accounts', newAccounts);
  };

  // Process emails: fetch from Gmail API, generate summaries, categorize, and save to database
  const processEmails = async (userDataParam = null) => {
    setProcessing(true);
    console.log('processEmails() running');
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    
    // Use provided userData or get from state/localStorage
    const userEmail = userDataParam?.email || user?.email;
    
    if (!userEmail) {
      console.error('processEmails: No user email available');
      return;
    }
    
    try {
      // Calculate timestamp (e.g., 30 days ago by default)
      const daysBack = 30;
      const maxResults = 10;
      const timestamp = new Date();
      timestamp.setDate(timestamp.getDate() - daysBack);
      
      const requestBody = {
        gmail_address: userEmail,
        timestamp: timestamp.toISOString(),
        max_results: maxResults
      };
      
      console.log('Calling /emails/process endpoint with:', requestBody);
      
      const response = await fetch(`${apiUrl}/emails/process`, {
        method: 'POST',
        credentials: 'include', // Important: Include cookies for authentication
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log('Response from /emails/process endpoint:', result);
        
       
        // call   await importEmail( ); with each of the email in the result array
        for (const email of result) {
          await importEmail(email);
        }
    
        setProcessing(false);

        if (result.message) {
          console.log(`Message: ${result.message}`);
        }
        if (result.length !== undefined) {
          console.log(`Emails processed: ${result.length}`);
        }

        if (result.errors && result.errors.length > 0) {
          console.warn('Errors during processing:', result.errors);
        }
        
        // If result is an array (emails), update state
        if (Array.isArray(result)) {
          console.log(`Total emails returned: ${result.length}`);
          
          // You can process the emails array here if needed
        }
        
        return result;
      } else {
        const errorData = await response.json();
        console.error('Error from /emails/process endpoint:', response.status, errorData);
        
        if (response.status === 401) {
          // Session expired - sign out user
          setUser(null);
          localStorage.clear();
        } else if (response.status === 403) {
          console.error('Gmail API access not configured. Please grant Gmail API access permissions.');
        }
        
        throw new Error(errorData.detail || `Error processing emails: ${response.statusText}`);
      }
    } catch (error) {
      console.error('Error calling /emails/process endpoint:', error);
      throw error;
    }
  };

  const fetchInboxEmails = async (userDataParam = null) => {
    console.log('fetchInboxEmails() running');
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    
    // Use provided userData or get from state/localStorage
    const userEmail = userDataParam?.email || user?.email;
    
    if (!userEmail) {
      console.error('fetchInboxEmails: No user email available');
      return;
    }
    
    try {
      // Calculate timestamp (e.g., 30 days ago)
      const timestamp = new Date();
      timestamp.setDate(timestamp.getDate() - 30); // Get emails from last 30 days
      
      const requestBody = {
        gmail_address: userEmail,
        timestamp: timestamp.toISOString(),
        max_results: 100
      };
      
      console.log('Calling /emails/inbox endpoint with:', requestBody);
      
      const response = await fetch(`${apiUrl}/emails/inbox`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      });
      
      if (response.ok) {
        const emails = await response.json();
        console.log('Response from /emails/inbox endpoint:', emails);
        console.log(`Total emails fetched: ${emails.length}`);
        emails.forEach((email, index) => {
          console.log(`Email ${index + 1}:`, {
            id: email.id,
            subject: email.subject,
            sender: email.sender,
            received_at: email.received_at,
          });
        });
      } else {
        const errorData = await response.json();
        console.error('Error from /emails/inbox endpoint:', response.status, errorData);
      }
    } catch (error) {
      console.error('Error calling /emails/inbox endpoint:', error);
    }
  };

  const handleSignOut = async () => {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    
    try {
      // Call logout endpoint to clear cookie on server
      await fetch(`${apiUrl}/logout`, {
        method: 'POST',
        credentials: 'include', // Include cookies in request
      });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear local state and storage
      setUser(null);
      setAccounts([]);
      setCategories([]);
      setEmails([]);
      setSelectedCategory(null);
      localStorage.clear();
    }
  };

  const addCategory = () => {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

    if (newCategory.name && newCategory.description) {
      const categoryData = {
        name: newCategory.name,
        description: newCategory.description,
      };

      fetch(`${apiUrl}/categories`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Include cookies in request
        body: JSON.stringify(categoryData),
      })
        .then(response => {
          if (!response.ok) {
            return response.json().then(err => {
              throw new Error(JSON.stringify(err));
            });
          }
          return response.json();
        })
        .then(data => {
          const category = {
            id: data.id.toString(),
            name: data.name,
            description: data.description,
            emailCount: 0,
          };
          const updated = [...categories, category];
          setCategories(updated);
          saveData('categories', updated);
          setNewCategory({ name: '', description: '' });
          setShowCategoryForm(false);
        })
        .catch(error => {
          console.error('Error adding category:', error);
        });
    }
  };

  const deleteCategory = (id) => {
    const updated = categories.filter(c => c.id !== id);
    setCategories(updated);
    saveData('categories', updated);

    const updatedEmails = emails.filter(e => e.categoryId !== id);
    setEmails(updatedEmails);
    saveData('emails', updatedEmails);

    if (selectedCategory?.id === id) {
      setSelectedCategory(null);
    }
  };

  const categorizeEmail = async (email) => {
    const categoryMatch = categories.find(c =>
      email.subject.toLowerCase().includes(c.name.toLowerCase()) ||
      email.body.toLowerCase().includes(c.name.toLowerCase())
    );

    return {
      categoryId: categoryMatch?.id || categories[0]?.id || null,
      summary: `This email discusses ${email.subject.toLowerCase()}. Key points include important updates and action items that may require your attention.`
    };
  };

  const importEmail = async (rawEmail) => {
    const { categoryId, summary } = await categorizeEmail(rawEmail);

    const email = {
      id: Date.now().toString(),
      ...rawEmail,
      categoryId,
      summary,
      archived: true,
      importedAt: new Date().toISOString()
    };

    const updated = [...emails, email];
    setEmails(updated);
    saveData('emails', updated);

    const updatedCategories = categories.map(c =>
      c.id === categoryId
        ? { ...c, emailCount: updated.filter(e => e.categoryId === c.id).length }
        : c
    );
    setCategories(updatedCategories);
    saveData('categories', updatedCategories);
  };

  const simulateNewEmail = async () => {
    setProcessing(true);
    const sampleEmails = [
      {
        subject: 'Weekly Tech Newsletter - AI Advances',
        from: 'newsletter@tech.com',
        body: 'Check out the latest in technology news this week including breakthrough in AI...',
        receivedAt: new Date().toISOString()
      },
      {
        subject: 'Your Monthly Statement is Ready',
        from: 'billing@company.com',
        body: 'Your statement for this month is now available for review...',
        receivedAt: new Date().toISOString()
      },
      {
        subject: 'Team Meeting Tomorrow at 2 PM',
        from: 'manager@work.com',
        body: 'Reminder about our team sync meeting scheduled for tomorrow...',
        receivedAt: new Date().toISOString()
      }
    ];

    const randomEmail = sampleEmails[Math.floor(Math.random() * sampleEmails.length)];
    await importEmail(randomEmail);
    setProcessing(false);
  };

  const addAccount = () => {
    const newEmail = prompt('Enter Gmail address to connect:');
    if (newEmail) {
      const updated = [...accounts, { email: newEmail, connected: true }];
      setAccounts(updated);
      saveData('accounts', updated);
    }
  };

  const toggleEmailSelection = (emailId) => {
    setSelectedEmails(prev =>
      prev.includes(emailId)
        ? prev.filter(id => id !== emailId)
        : [...prev, emailId]
    );
  };

  const selectAllEmails = () => {
    const categoryEmails = emails.filter(e => e.categoryId === selectedCategory?.id);
    const allIds = categoryEmails.map(e => e.id);
    setSelectedEmails(allIds.length === selectedEmails.length ? [] : allIds);
  };

  const bulkDelete = async () => {
    setProcessing(true);
    const updated = emails.filter(e => !selectedEmails.includes(e.id));
    setEmails(updated);
    saveData('emails', updated);

    const updatedCategories = categories.map(c => ({
      ...c,
      emailCount: updated.filter(e => e.categoryId === c.id).length
    }));
    setCategories(updatedCategories);
    saveData('categories', updatedCategories);

    setSelectedEmails([]);
    setProcessing(false);
  };

  const bulkUnsubscribe = async () => {
    setProcessing(true);
    alert(`Unsubscribe requested for ${selectedEmails.length} emails`);
    await bulkDelete();
    setProcessing(false);
  };

  const handleEmailClick = (email) => {
    setSelectedEmailDetail(email);
  };

  const handleDeleteEmailDetail = async () => {
    if (selectedEmailDetail) {
      setProcessing(true);
      const updated = emails.filter(e => e.id !== selectedEmailDetail.id);
      setEmails(updated);
      saveData('emails', updated);

      const updatedCategories = categories.map(c => ({
        ...c,
        emailCount: updated.filter(e => e.categoryId === c.id).length
      }));
      setCategories(updatedCategories);
      saveData('categories', updatedCategories);

      setSelectedEmailDetail(null);
      setProcessing(false);
    }
  };

  const handleUnsubscribeEmailDetail = async () => {
    if (selectedEmailDetail) {
      setProcessing(true);
      alert(`Unsubscribe requested for: ${selectedEmailDetail.subject}`);
      await handleDeleteEmailDetail();
    }
  };

  if (!user) {
    return <LoginScreen onLogin={handleLogin} />;
  }

  if (selectedCategory) {
    const categoryEmails = emails.filter(e => e.categoryId === selectedCategory.id);

    // Show email detail page if an email is selected
    if (selectedEmailDetail) {
      return (
        <EmailDetailPage
          email={selectedEmailDetail}
          user={user}
          onBack={() => setSelectedEmailDetail(null)}
          onDelete={handleDeleteEmailDetail}
          onUnsubscribe={handleUnsubscribeEmailDetail}
          processing={processing}
        />
      );
    }

    // Show category email list
    return (
      <CategoryView
        category={selectedCategory}
        emails={categoryEmails}
        selectedEmails={selectedEmails}
        onBack={() => { setSelectedCategory(null); setSelectedEmails([]); }}
        onToggleEmail={toggleEmailSelection}
        onSelectAll={selectAllEmails}
        onBulkDelete={bulkDelete}
        onBulkUnsubscribe={bulkUnsubscribe}
        onEmailClick={handleEmailClick}
        processing={processing}
      />
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header user={user} onSignOut={handleSignOut} />

      <main className="max-w-7xl mx-auto p-6 space-y-6">
        <ConnectedAccounts accounts={accounts} onAddAccount={addAccount} />

        <CategoriesList
          categories={categories}
          showForm={showCategoryForm}
          newCategory={newCategory}
          onNewCategoryChange={setNewCategory}
          onAddCategory={addCategory}
          onCancelForm={() => { setShowCategoryForm(false); setNewCategory({ name: '', description: '' }); }}
          onShowForm={() => setShowCategoryForm(true)}
          onSelectCategory={setSelectedCategory}
          onDeleteCategory={deleteCategory}
        />

        <DemoSection
          onSimulate={simulateNewEmail}
          processing={processing}
          categoriesExist={categories.length > 0}
        />
      </main>
    </div>
  );
}