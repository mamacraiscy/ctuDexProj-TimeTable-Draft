import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './CreateRoomUtil.css';

const CreateRoomUtil = () => {
  // Define state variables
  const [selectedRoom, setSelectedRoom] = useState('');
  const [subjectName, setSubjectName] = useState('');
  const [appointmentDuration, setAppointmentDuration] = useState('30 minutes');
  const [availabilityOption, setAvailabilityOption] = useState('doesNotRepeat');
  const [customDuration, setCustomDuration] = useState('');
  const [customDurationUnit, setCustomDurationUnit] = useState('minutes');
  const [customAvailability, setCustomAvailability] = useState('');
  const [isDurationModalOpen, setIsDurationModalOpen] = useState(false);
  const [isAvailabilityModalOpen, setIsAvailabilityModalOpen] = useState(false);

  // Data options
  const [roomOptions, setRoomOptions] = useState([]);
  const [subjectOptions, setSubjectOptions] = useState([]);
  const [departmentOptions, setDepartmentOptions] = useState([]);
  const [yearLevelOptions, setYearLevelOptions] = useState([]);
  const [sectionOptions, setSectionOptions] = useState([]);

  // Loading and error states
  const [loading, setLoading] = useState({ rooms: false, courses: false, departments: false, sections: false });
  const [error, setError] = useState(null);

  // Fetch rooms on component mount
  useEffect(() => {
    const fetchRooms = async () => {
      setLoading((prev) => ({ ...prev, rooms: true }));
      try {
        const response = await axios.get('http://localhost:8000/api/rooms');
        setRoomOptions(response.data);
      } catch (err) {
        console.error("Error fetching rooms:", err);
        setError("Failed to load rooms");
      } finally {
        setLoading((prev) => ({ ...prev, rooms: false }));
      }
    };
    fetchRooms();
  }, []);

  // Fetch courses based on selected room
  useEffect(() => {
    if (selectedRoom) {
      const fetchCourses = async () => {
        setLoading((prev) => ({ ...prev, courses: true }));
        try {
          const response = await axios.get('http://localhost:8000/api/get_courses_by_room/', {
            params: { room_number: selectedRoom },
          });
          setSubjectOptions(response.data);
        } catch (err) {
          console.error("Error fetching courses:", err);
          setError("Failed to load courses");
        } finally {
          setLoading((prev) => ({ ...prev, courses: false }));
        }
      };

      const fetchDepartments = async () => {
        setLoading((prev) => ({ ...prev, departments: true }));
        try {
          const response = await axios.get('http://localhost:8000/api/courses'); // Assuming courses contain department data
          setDepartmentOptions([...new Set(response.data.map(course => course.department))]);
        } catch (err) {
          console.error("Error fetching departments:", err);
          setError("Failed to load departments");
        } finally {
          setLoading((prev) => ({ ...prev, departments: false }));
        }
      };

      const fetchSections = async () => {
        setLoading((prev) => ({ ...prev, sections: true }));
        try {
          const response = await axios.get('http://localhost:8000/api/sections'); // Assuming sections data is available here
          setYearLevelOptions([...new Set(response.data.map(section => section.year_level))]);
          setSectionOptions(response.data);
        } catch (err) {
          console.error("Error fetching sections:", err);
          setError("Failed to load sections");
        } finally {
          setLoading((prev) => ({ ...prev, sections: false }));
        }
      };

      fetchCourses();
      fetchDepartments();
      fetchSections();
    } else {
      setSubjectOptions([]);
      setDepartmentOptions([]);
      setYearLevelOptions([]);
      setSectionOptions([]);
    }
  }, [selectedRoom]);

  const handleDropdownChange = (setter) => (event) => {
    setter(event.target.value);
    setSubjectOptions([]);  // Reset subject options when a new room is selected
    setSubjectName('');  // Reset subject name
  };

  const handleCustomSave = (setter, input, validationMsg, closeModal) => {
    if (input.trim()) {
      setter(input);
      closeModal();
    } else {
      alert(validationMsg);
    }
  };

  return (
    <div className="room-utilization">
      <div className="sidebar">
        <h3>Room Utilization Settings</h3>

        {/* Room Name Section */}
        <div className="section">
          <label>Room Name:</label>
          <select value={selectedRoom} onChange={handleDropdownChange(setSelectedRoom)}>
            <option value="">Select Room</option>
            {roomOptions.map((room) => (
              <option key={room.room_id} value={room.room_number}>
                {`${room.room_number} - ${room.room_type}`}
              </option>
            ))}
          </select>
        </div>

        {/* Subject (Course) Name Section */}
        <div className="section">
          <label>Subject (Course) Name:</label>
          <select value={subjectName} onChange={(e) => setSubjectName(e.target.value)}>
            <option value="">Select a course</option>
            {subjectOptions.map((course) => (
              <option key={course.course_id} value={course.course_name}>{course.course_name}</option>
            ))}
          </select>
        </div>

        {/* Department Dropdown */}
        <div className="section">
          <label>Department:</label>
          <select value={subjectName} onChange={(e) => setSubjectName(e.target.value)}>
            <option value="">Select Department</option>
            {departmentOptions.map((department, index) => (
              <option key={index} value={department}>{department}</option>
            ))}
          </select>
        </div>

        {/* Year Level Dropdown */}
        <div className="section">
          <label>Year Level:</label>
          <select value={subjectName} onChange={(e) => setSubjectName(e.target.value)}>
            <option value="">Select Year Level</option>
            {yearLevelOptions.map((yearLevel, index) => (
              <option key={index} value={yearLevel}>{yearLevel}</option>
            ))}
          </select>
        </div>

        {/* Section Dropdown */}
        <div className="section">
          <label>Section:</label>
          <select value={subjectName} onChange={(e) => setSubjectName(e.target.value)}>
            <option value="">Select Section</option>
            {sectionOptions.map((section) => (
              <option key={section.section_id} value={section.section_name}>
                {section.section_name}
              </option>
            ))}
          </select>
        </div>

        {/* Appointment Duration Section */}
        <div className="section">
          <label>Appointment Duration:</label>
          <select value={appointmentDuration} onChange={(e) => e.target.value === 'custom' ? setIsDurationModalOpen(true) : setAppointmentDuration(e.target.value)}>
            <option value="15 minutes">15 minutes</option>
            <option value="30 minutes">30 minutes</option>
            <option value="1 hour">1 hour</option>
            <option value="1.5 hours">1.5 hours</option>
            <option value="2 hours">2 hours</option>
            <option value="custom">Custom</option>
          </select>
        </div>

        {/* General Availability Section */}
        <div className="section">
          <label>General Availability:</label>
          <select value={availabilityOption} onChange={(e) => e.target.value === 'custom' ? setIsAvailabilityModalOpen(true) : setAvailabilityOption(e.target.value)}>
            <option value="doesNotRepeat">Does not repeat</option>
            <option value="repeatWeekly">Repeat weekly</option>
            <option value="custom">Custom</option>
          </select>
        </div>
      </div>

      {/* Custom Duration Modal */}
      {isDurationModalOpen && (
        <div className="modal-overlay">
          <div className="modal">
            <h4>Select Custom Appointment Duration</h4>
            <input type="number" value={customDuration} onChange={(e) => setCustomDuration(e.target.value)} placeholder="Enter duration" min="1" />
            <select value={customDurationUnit} onChange={(e) => setCustomDurationUnit(e.target.value)}>
              <option value="minutes">Minutes</option>
              <option value="hours">Hours</option>
            </select>
            <button onClick={() => handleCustomSave(setAppointmentDuration, `${customDuration} ${customDurationUnit}`, "Please enter a valid custom duration.", () => setIsDurationModalOpen(false))}>Save Duration</button>
          </div>
        </div>
      )}

      {/* Custom Availability Modal */}
      {isAvailabilityModalOpen && (
        <div className="modal-overlay">
          <div className="modal">
            <h4>Enter Custom Availability</h4>
            <input type="text" value={customAvailability} onChange={(e) => setCustomAvailability(e.target.value)} placeholder="Enter custom availability" />
            <button onClick={() => handleCustomSave(setAvailabilityOption, customAvailability, "Please enter valid availability.", () => setIsAvailabilityModalOpen(false))}>Save Availability</button>
          </div>
        </div>
      )}

      {/* Error Message Display */}
      {error && <p className="error-message">{error}</p>}
    </div>
  );
};

export default CreateRoomUtil;
