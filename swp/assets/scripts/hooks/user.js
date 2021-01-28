class User {
    constructor(
        id,
        email,
        name = '',
        firstName = '',
        lastName = '',
        isActive = false,
        isStaff = false,
        isSuperUser = false,
        permissions = null,
        groups = null,
    ) {
        this.id = id;
        this.email = email;
        this.name = name;
        this.firstName = firstName;
        this.lastName = lastName;
        this.isActive = isActive;
        this.isStaff = isStaff;
        this.isSuperUser = isSuperUser;
        this.permissions = permissions || [];
        this.groups = groups || [];
    }

    static fromData(data) {
        return new User(
            data.id,
            data.email,
            data.name,
            data.first_name,
            data.last_name,
            data.is_active,
            data.is_staff,
            data.is_superuser,
            data.permissions,
            data.groups,
        );
    }

    hasPerm(permission) {
        return this.permissions.includes(permission);
    }

    canViewAdmin() {
        return this.isActive && this.isStaff && this.isSuperUser;
    }
}

const UserData = (() => {
    const node = document.getElementById('user-data');
    const data = JSON.parse(node.textContent);
    node.parentNode.removeChild(node);

    return User.fromData(data);
})();

export const useUser = () => UserData;

export const usePermission = perm => useUser().hasPerm(perm);
