
package org.dmg.pmml;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlEnum;
import javax.xml.bind.annotation.XmlEnumValue;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.XmlValue;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;
import org.dmg.pmml.adapters.IntegerAdapter;


/**
 * <p>Java class for anonymous complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType>
 *   &lt;simpleContent>
 *     &lt;extension base="&lt;http://www.w3.org/2001/XMLSchema>string">
 *       &lt;attribute name="n" type="{http://www.dmg.org/PMML-4_2}INT-NUMBER" />
 *       &lt;attribute name="type" use="required">
 *         &lt;simpleType>
 *           &lt;restriction base="{http://www.w3.org/2001/XMLSchema}string">
 *             &lt;enumeration value="int"/>
 *             &lt;enumeration value="real"/>
 *             &lt;enumeration value="string"/>
 *           &lt;/restriction>
 *         &lt;/simpleType>
 *       &lt;/attribute>
 *     &lt;/extension>
 *   &lt;/simpleContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "value"
})
@XmlRootElement(name = "Array", namespace = "http://www.dmg.org/PMML-4_2")
public class Array
    extends PMMLObject
{

    @XmlAttribute(name = "n")
    @XmlJavaTypeAdapter(IntegerAdapter.class)
    protected Integer n;
    @XmlAttribute(name = "type", required = true)
    protected Array.Type type;
    @XmlValue
    protected String value;

    public Array() {
        super();
    }

    public Array(final Array.Type type, final String value) {
        super();
        this.type = type;
        this.value = value;
    }

    /**
     * Gets the value of the n property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public Integer getN() {
        return n;
    }

    /**
     * Sets the value of the n property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setN(Integer value) {
        this.n = value;
    }

    /**
     * Gets the value of the type property.
     * 
     * @return
     *     possible object is
     *     {@link Array.Type }
     *     
     */
    public Array.Type getType() {
        return type;
    }

    /**
     * Sets the value of the type property.
     * 
     * @param value
     *     allowed object is
     *     {@link Array.Type }
     *     
     */
    public void setType(Array.Type value) {
        this.type = value;
    }

    /**
     * Gets the value of the value property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getValue() {
        return value;
    }

    /**
     * Sets the value of the value property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setValue(String value) {
        this.value = value;
    }

    public Array withN(Integer value) {
        setN(value);
        return this;
    }

    public Array withType(Array.Type value) {
        setType(value);
        return this;
    }

    public Array withValue(String value) {
        setValue(value);
        return this;
    }

    @Override
    public VisitorAction accept(Visitor visitor) {
        VisitorAction status = visitor.visit(this);
        visitor.pushParent(this);
        visitor.popParent();
        if (status == VisitorAction.TERMINATE) {
            return VisitorAction.TERMINATE;
        }
        return VisitorAction.CONTINUE;
    }


    /**
     * <p>Java class for null.
     * 
     * <p>The following schema fragment specifies the expected content contained within this class.
     * <p>
     * <pre>
     * &lt;simpleType>
     *   &lt;restriction base="{http://www.w3.org/2001/XMLSchema}string">
     *     &lt;enumeration value="int"/>
     *     &lt;enumeration value="real"/>
     *     &lt;enumeration value="string"/>
     *   &lt;/restriction>
     * &lt;/simpleType>
     * </pre>
     * 
     */
    @XmlType(name = "")
    @XmlEnum
    public enum Type {

        @XmlEnumValue("int")
        INT("int"),
        @XmlEnumValue("real")
        REAL("real"),
        @XmlEnumValue("string")
        STRING("string");
        private final String value;

        Type(String v) {
            value = v;
        }

        public String value() {
            return value;
        }

        public static Array.Type fromValue(String v) {
            for (Array.Type c: Array.Type.values()) {
                if (c.value.equals(v)) {
                    return c;
                }
            }
            throw new IllegalArgumentException(v);
        }

    }

}
